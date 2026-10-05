"""The figure-level archive must validate in any fresh Git checkout."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / 'paper_figures/figure_s14'


def test_committed_s14_source_hashes_and_sizes():
    manifest = json.loads((PAPER / 'source_data_manifest.json').read_text())
    paths = [entry['path'] for entry in manifest['files']]
    assert len(paths) == len(set(paths)) == 138
    assert set(paths) == {path.relative_to(PAPER).as_posix()
                         for path in (PAPER / 'source_data').rglob('*') if path.is_file()}
    for entry in manifest['files']:
        data = (PAPER / entry['path']).read_bytes()
        assert len(data) == entry['bytes'], entry['path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']


def plotting_module():
    spec = importlib.util.spec_from_file_location('s14_integrity_fixture', PAPER / 'plot_figure_s14.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_s14_rejects_corruption_and_unlisted_inputs(tmp_path, monkeypatch):
    # Plotting dependencies are separate from the main matching environment.
    pytest.importorskip('pandas')
    module = plotting_module()
    data = tmp_path / 'source_data'
    data.mkdir()
    path = data / 'fixture.csv'
    original = b'value\n1\n'
    path.write_bytes(original)
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'files': [{'path': 'source_data/fixture.csv',
        'bytes': len(original), 'sha256': hashlib.sha256(original).hexdigest()}]}))
    monkeypatch.setattr(module, 'SCRIPT_DIR', tmp_path)
    monkeypatch.setattr(module, 'SOURCE_DATA', data)
    monkeypatch.setattr(module, 'SOURCE_MANIFEST', manifest)
    module.validate_source_data()
    path.write_bytes(b'value\n2\n')
    with pytest.raises(RuntimeError, match='SHA-256 mismatch'):
        module.validate_source_data()
    path.write_bytes(original)
    (data / 'unlisted.csv').write_bytes(original)
    with pytest.raises(RuntimeError, match='coverage mismatch'):
        module.validate_source_data()


def test_s14_tiff_export_preserves_every_png_pixel(tmp_path):
    pytest.importorskip('pandas')
    from PIL import Image
    import numpy as np
    module = plotting_module()
    data = np.arange(8 * 11 * 4, dtype=np.uint8).reshape(8, 11, 4)
    png, tiff = tmp_path / 'fixture.png', tmp_path / 'fixture.tif'
    Image.fromarray(data).save(png, dpi=(600, 600))
    module.save_lossless_tiff(png, tiff)
    with Image.open(tiff) as image:
        assert image.tobytes() == data.tobytes()
        assert image.info['compression'] == 'tiff_lzw'
        assert tuple(image.info['dpi']) == (600., 600.)


@pytest.mark.parametrize('absolute', [False, True])
def test_s14_export_record_survives_relocation(tmp_path, monkeypatch, absolute):
    pytest.importorskip('pandas')
    import shutil
    module = plotting_module()
    monkeypatch.chdir(tmp_path)
    folder = Path('first/exports')
    folder.mkdir(parents=True)
    path = folder / 'panel.png'
    path.write_bytes(b'exported figure bytes')
    if absolute:
        path, folder = path.resolve(), folder.resolve()
    record = module.export_record(path, folder)
    assert record['path'] == 'panel.png'
    shutil.copytree(folder, tmp_path / 'relocated')
    observed = tmp_path / 'relocated' / record['path']
    assert hashlib.sha256(observed.read_bytes()).hexdigest() == record['sha256']
