"""Prevent unrelated analyses and personal default paths entering this release."""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]


def test_matching_source_tree_has_no_uv_nir_archive():
    assert not (REPO / 'paper_figures/figure_s14').exists()
    assert not (REPO / 'tests/test_s14_source_integrity.py').exists()
    assert 's14-reproduction' not in (REPO / '.github/workflows/ci.yml').read_text()


def test_matching_sources_have_no_personal_default_paths():
    pattern = re.compile(rb'[A-Za-z]:[\\/]+Users[\\/]+|/(?:home|Users)/', re.I)
    for path in REPO.rglob('*.py'):
        assert pattern.search(path.read_bytes()) is None, path.relative_to(REPO)
