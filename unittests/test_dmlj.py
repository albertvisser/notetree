import pytest
import notetree.json_dml as dmlj


def test_load_1(monkeypatch, capsys, tmp_path):
    "test file does not exist"
    dest = tmp_path / 'load1.json'
    try:
        dest.unlink()
    except FileNotFoundError:
        pass
    assert dmlj.load_file(dest) == {}


def test_load_2(monkeypatch, capsys, tmp_path):
    "test file exists but cannot be loaded"
    def mock_load(*args):
        raise RuntimeError
    dest = tmp_path / 'load2.json'
    dest.touch()
    monkeypatch.setattr(dmlj.json, 'load', mock_load)
    with pytest.raises(RuntimeError):
        dmlj.load_file(dest)


def test_load_3(monkeypatch, capsys, tmp_path):
    "missing Application option"
    dest = tmp_path / 'load3.json'
    dest.touch()
    monkeypatch.setattr(dmlj.json, 'load', lambda x: {})
    with pytest.raises(EOFError):
        dmlj.load_file(dest)


def test_load_4(monkeypatch, capsys, tmp_path):
    "wrong Application option"
    dest = tmp_path / 'load4.json'
    dest.touch()
    monkeypatch.setattr(dmlj.json, 'load', lambda x: {0: {'Application': 'x'}})
    with pytest.raises(EOFError):
        dmlj.load_file(dest)


def test_load_5(monkeypatch, capsys, tmp_path):
    "no errors"
    dest = tmp_path / 'load5.json'
    dest.touch()
    conf = {'Application': 'NoteTree', 'ScreenSize': (9, 6), 'Selection': [10, 1], 'SashPosition': [55]}
    monkeypatch.setattr(dmlj.json, 'load', lambda x: {0: conf, '01-01-0001 00:00:00': 'x'})
    assert dmlj.load_file(dest) == {0: {'Application': 'NoteTree', 'ScreenSize': (9, 6),
                                       'Selection': (10,1), 'SashPosition': (55,)},
                                       '01-01-0001 00:00:00': ('x',)}    # is dit text + keywords?


def test_save(monkeypatch, capsys, tmp_path):
    def mock_save(*args, **kwargs):
        print('called json.dump for data `{}`'.format(args[0]))
    dest = tmp_path / 'save.json'
    data = 'nt_data'
    monkeypatch.setattr(dmlj.json, 'dump', mock_save)
    dmlj.save_file(dest, data)
    assert capsys.readouterr().out == 'called json.dump for data `nt_data`\n'
