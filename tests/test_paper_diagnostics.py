from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from microscopy_matching.pipeline import FREE_MATCHING_SEARCH, PipelineRun
from paper_figures import diagnostics


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
