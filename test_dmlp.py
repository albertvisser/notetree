import pytest
import notetree.pickle_dml as dmlp


def test_load_1(monkeypatch, capsys, tmp_path):
    "test file does not exist"
    dest = tmp_path / 'load1.pck'
    try:
        dest.unlink()
    except FileNotFoundError:
        pass
    assert dmlp.load_file(dest) == {}


def test_load_2(monkeypatch, capsys, tmp_path):
    "test file exists but cannot be loaded"
    def mock_load(*args):
        raise RuntimeError
    dest = tmp_path / 'load2.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', mock_load)
    with pytest.raises(RuntimeError):
        dmlp.load_file(dest)


def test_load_3(monkeypatch, capsys, tmp_path):
    "missing Application option"
    dest = tmp_path / 'load3.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {})
    with pytest.raises(EOFError):
        dmlp.load_file(dest)


def test_load_4(monkeypatch, capsys, tmp_path):
    "wrong Application option"
    dest = tmp_path / 'load4.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {0: {'Application': 'x'}})
    with pytest.raises(EOFError):
        dmlp.load_file(dest)


def test_load_5(monkeypatch, capsys, tmp_path):
    "no errors"
    dest = tmp_path / 'load5.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {0: {'Application': 'NoteTree'}, 1: 'x'})
    assert dmlp.load_file(dest) == {0: {'Application': 'NoteTree'}, 1: 'x'}


def test_save(monkeypatch, capsys, tmp_path):
    def mock_save(*args, **kwargs):
        print('called pickle.dump for data `{}`'.format(args[0]))
    dest = tmp_path / 'save.pck'
    data = 'nt_data'
    monkeypatch.setattr(dmlp.pck, 'dump', mock_save)
    dmlp.save_file(dest, data)
    assert capsys.readouterr().out == 'called pickle.dump for data `nt_data`\n'