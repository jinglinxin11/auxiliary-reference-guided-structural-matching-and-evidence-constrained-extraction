from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from microscopy_matching.pipeline import FREE_MATCHING_SEARCH, PipelineRun
from paper_figures import diagnostics
import json


def test_configure_arial_discovers_installed_fonts(monkeypatch, tmp_path) -> None:
    regular, bold = tmp_path / "arial.ttf", tmp_path / "arialbd.ttf"
    regular.touch()
    bold.touch()
    requests, registered = [], []

    def findfont(properties, *, fallback_to_default):
        requests.append((properties.get_family(), properties.get_weight(), fallback_to_default))
        return str(bold if properties.get_weight() == "bold" else regular)

    monkeypatch.setattr(diagnostics.font_manager, "findfont", findfont)
    monkeypatch.setattr(diagnostics.font_manager.fontManager, "addfont", registered.append)
    assert diagnostics.configure_arial() == regular
    assert requests == [(["Arial"], "normal", False), (["Arial"], "bold", False)]
    assert registered == [str(regular), str(bold)]


def test_configure_arial_rejects_missing_family(monkeypatch) -> None:
    def findfont(*args, **kwargs):
        raise ValueError("Font family unavailable")

    monkeypatch.setattr(diagnostics.font_manager, "findfont", findfont)
    with pytest.raises(RuntimeError, match="Arial and Arial Bold are required"):
        diagnostics.configure_arial()


def test_configure_arial_rejects_regular_font_as_bold(monkeypatch, tmp_path) -> None:
    regular = tmp_path / "arial.ttf"
    regular.touch()
    monkeypatch.setattr(diagnostics.font_manager, "findfont", lambda *args, **kwargs: str(regular))
    with pytest.raises(RuntimeError, match="Arial and Arial Bold are required"):
        diagnostics.configure_arial()


def test_paper_diagnostics_uses_free_grid_and_pipeline_scoring_config(monkeypatch) -> None:
    paths = tuple(Path(f"{index}.png") for index in range(4))
    structures = tuple(object() for _ in range(4))
    calibrations = tuple(SimpleNamespace(confidence=1.0) for _ in range(4))
    matches = tuple(tuple(SimpleNamespace(score=0.5, physical_scale_available=True)
                          for _ in range(4)) for _ in range(4))
    run = PipelineRun(
        Path("."), Path("."), (), (), (), paths, paths,
        structures, structures, structures, structures,
        calibrations, calibrations, matches,
    )
    landscape_calls, rerun_calls = [], []

    def landscape(*args, **kwargs):
        landscape_calls.append(kwargs)
        return np.zeros((41, 41))

    def refine(*args, **kwargs):
        rerun_calls.append(kwargs)
        return SimpleNamespace(score=kwargs["config"].generic_scale_max / 2)

    monkeypatch.setattr(diagnostics, "translation_score_landscape", landscape)
    monkeypatch.setattr(diagnostics, "refine_candidate", refine)
    monkeypatch.setattr(diagnostics, "corridor_radius_metrics", lambda *args: tuple(
        diagnostics.RadiusMetric(int(radius), 0.1, 0.2, 0.15) for radius in args[3]
    ))
    context = diagnostics.build_paper_diagnostics(run)
    assert landscape_calls == [{"physical_prior_confidence": 0.0, "config": FREE_MATCHING_SEARCH}]
    assert len(rerun_calls) == 12
    assert [call["config"].generic_scale_max for call in rerun_calls] == [1.6] * 4 + [1.75] * 4 + [1.9] * 4
    assert all(call["physical_scale_prior"] is None for call in rerun_calls)
    assert all(call["physical_prior_confidence"] == 0.0 for call in rerun_calls)
    assert all(call["config"].generic_scale_count == 7 for call in rerun_calls)
    assert all(call["config"].physical_prior_weight == 0.0 for call in rerun_calls)
    assert context.search_bound_scores[:, 0] == pytest.approx([0.8, 0.875, 0.95])


@pytest.mark.parametrize('target_um,reference_um', [(200., 500.), (400., 1000.)])
def test_native_calibration_metadata_uses_actual_lengths(tmp_path, target_um, reference_um):
    path = tmp_path / 'input.png'
    path.write_bytes(b'input hash fixture')

    def calibration(length):
        return SimpleNamespace(pixels_per_um=2., confidence=1., source='explicit',
            scale_bar_length_um=length, scale_bar_pixels=2*length,
            bar_bbox_xyxy=None, annotation_bbox_xyxy=None)

    image = np.zeros((10, 10, 3), dtype=np.uint8)
    run = SimpleNamespace(pair_rows=[{'x': 1}], summary_rows=[{'x': 1}],
        search_config=FREE_MATCHING_SEARCH, target_paths=[path], reference_paths=[path],
        target_calibrations=[calibration(target_um)], reference_calibrations=[calibration(reference_um)],
        target_images=[image], target_structures=[SimpleNamespace(image=image)])
    context = SimpleNamespace(run=run, radius_metrics_by_target=[], radius_metrics=[],
        translation_offsets=np.array([0]), translation_scores=np.array([[0.]]),
        search_bound_values=np.array([1.6]), search_bound_scores=np.array([[0.]*4]),
        reference_labels=['S','T','U','Z'], target_labels=['a','b','c','d'],
        selected_indices=[0], representative_index=0)
    diagnostics.write_diagnostic_tables(context, tmp_path / 'out')
    manifest = json.loads((tmp_path / 'out/diagnostics.json').read_text())
    convention = manifest['physical_scale_convention']
    assert convention['target_native_scale_bar_um'] == target_um
    assert convention['reference_native_scale_bar_um'] == reference_um
    assert convention['manuscript_display_scale_bar_um'] == 200.
    assert f'native {reference_um:g}-um reference' in convention['reference_display_transform']


def test_native_scale_metadata_rejects_inconsistent_or_invalid_lengths():
    for lengths in ([None], [float('nan')], [0.], [200., 500.]):
        with pytest.raises(RuntimeError, match='finite, positive and consistent'):
            diagnostics.native_scale_bar_length(
                [SimpleNamespace(scale_bar_length_um=value) for value in lengths], 'Target')
