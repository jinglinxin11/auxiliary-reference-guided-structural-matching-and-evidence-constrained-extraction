from pathlib import Path
from dataclasses import replace
from types import SimpleNamespace

import numpy as np
import pytest

import microscopy_matching.pipeline as pipeline

from microscopy_matching.pipeline import (
    DEFAULT_AUXILIARY_SCALE_BAR_UM,
    DEFAULT_TARGET_SCALE_BAR_UM,
    FREE_MATCHING_SEARCH,
    PipelineRun,
    SelectedMatch,
    minimal_results_payload,
)


@pytest.mark.parametrize("ppu", [None, 0.25, 2.5])
def test_calibration_is_never_forwarded_to_free_registration(tmp_path, monkeypatch, ppu) -> None:
    targets, references = tmp_path / "targets", tmp_path / "references"
    targets.mkdir()
    references.mkdir()
    for index in range(4):
        (targets / f"target_{index}.png").touch()
        (references / f"candidate_{index}.png").touch()
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    monkeypatch.setattr(pipeline, "read", lambda path: image)
    monkeypatch.setattr(pipeline, "resize_for_analysis", lambda value: value)
    monkeypatch.setattr(pipeline, "build_structure", lambda value: SimpleNamespace(image=value))
    monkeypatch.setattr(pipeline, "select_central_auxiliary_support", lambda value: value)
    calibration = SimpleNamespace(pixels_per_um=ppu, success=ppu is not None)
    monkeypatch.setattr(pipeline, "_calibrations", lambda values, length: [calibration] * 4)
    calls = []

    def refine(target, reference, **kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            score=0.5, scale=1.0, angle_deg=0.0, dx=0.0, dy=0.0,
            physical_scale_prior=None, physical_scale_score=None,
            physical_scale_available=kwargs["physical_scale_available"], topology_score=0.5,
        )

    monkeypatch.setattr(pipeline, "refine_candidate", refine)
    monkeypatch.setattr(pipeline, "_pair_row", lambda *args: {})
    monkeypatch.setattr(pipeline, "native_bbox", lambda *args: (1, 1, 7, 7))
    monkeypatch.setattr(pipeline, "_render_target_evidence", lambda *args: image)
    run = pipeline.run_pipeline(targets, references)
    assert len(calls) == 16
    assert all(call["physical_scale_prior"] is None for call in calls)
    assert all(call["physical_prior_confidence"] == 0.0 for call in calls)
    assert all(call["config"] == FREE_MATCHING_SEARCH for call in calls)
    assert all(row["physical_scale_mode"] == "report_only" for row in run.summary_rows)
    assert run.search_config == FREE_MATCHING_SEARCH


def test_free_pipeline_rejects_a_physical_prior_configuration() -> None:
    with pytest.raises(ValueError, match="physical-scale prior"):
        pipeline.run_pipeline(Path("."), Path("."), search_config=replace(
            FREE_MATCHING_SEARCH, physical_prior_weight=0.08,
        ))


def test_free_matching_restores_archived_generic_search_without_a_prior() -> None:
    assert DEFAULT_TARGET_SCALE_BAR_UM == 200.0
    assert DEFAULT_AUXILIARY_SCALE_BAR_UM == 500.0
    assert FREE_MATCHING_SEARCH.generic_scale_min == 0.70
    assert FREE_MATCHING_SEARCH.generic_scale_max == 1.60
    assert FREE_MATCHING_SEARCH.generic_scale_count == 7
    assert FREE_MATCHING_SEARCH.physical_residual_scale_range is None
    assert FREE_MATCHING_SEARCH.fine_scale_half_width == 0.14
    assert FREE_MATCHING_SEARCH.physical_prior_weight == 0.0


def test_minimal_results_payload_contains_only_final_result_references() -> None:
    row = {
        "target_id": "target_01",
        "selected_label": "S",
        "selected_score": 0.5,
        "runner_up_label": "T",
        "margin": 0.1,
        "analysis_scale": 1.0,
        "analysis_angle_deg": 0.0,
        "analysis_dx": 1.0,
        "analysis_dy": 2.0,
        "physical_scale_mode": "report_only",
        "target_scale_bar_um": 200.0,
        "auxiliary_scale_bar_um": 500.0,
        "physical_scale_prior": None,
        "physical_analysis_scale_residual": None,
        "physical_scale_score": None,
        "selected_native_bbox_xyxy": "1 2 3 4",
    }
    selection = SelectedMatch(
        target_index=0,
        candidate_index=0,
        target_path=Path("S.png"),
        candidate_path=Path("S.png"),
        target_original=np.zeros((1, 1, 3), dtype=np.uint8),
        target=None,  # type: ignore[arg-type]
        auxiliary=None,  # type: ignore[arg-type]
        match=None,  # type: ignore[arg-type]
        summary_row=row,
        rendered=np.zeros((1, 1, 3), dtype=np.uint8),
    )
    payload = minimal_results_payload(
        PipelineRun(Path("."), Path("."), (), (row,), (selection,))
    )

    assert payload["mode"] == "automatic_independent_free_matching"
    assert payload["binary_rule"] == "target_foreground_and_registered_auxiliary_corridor"
    assert payload["results"] == [
        {
            "target_id": "target_01",
            "selected_label": "S",
            "selected_score": 0.5,
            "runner_up_label": "T",
            "margin": 0.1,
            "analysis_transform": {"scale": 1.0, "angle_deg": 0.0, "dx": 1.0, "dy": 2.0},
            "physical_scale": {
                "mode": "report_only",
                "target_scale_bar_um": 200.0,
                "auxiliary_scale_bar_um": 500.0,
                "analysis_prior": None,
                "analysis_residual": None,
                "score": None,
            },
            "native_bbox_xyxy": "1 2 3 4",
            "presentation_file": "presentation/target_01_S.png",
            "binary_file": "binary/target_01_S.png",
        }
    ]
