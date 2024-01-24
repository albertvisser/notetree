"""unittests for ./notetree/pickle_dml.py
"""
import pytest
import notetree.pickle_dml as dmlp


def test_load_1(tmp_path):
    """unittest for pickle_dml.load: file does not exist
    """
    dest = tmp_path / 'load1.pck'
    dest.unlink(missing_ok=True)
    assert dmlp.load_file(dest) == {}


def test_load_2(monkeypatch, tmp_path):
    """unittest for pickle_dml.load: file exists but cannot be loaded
    """
    def mock_load(*args):
        """stub
        """
        raise RuntimeError
    dest = tmp_path / 'load2.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', mock_load)
    with pytest.raises(RuntimeError):
        dmlp.load_file(dest)


def test_load_3(monkeypatch, tmp_path):
    """unittest for pickle_dml.load: missing Application option
    """
    dest = tmp_path / 'load3.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {})
    with pytest.raises(EOFError):
        dmlp.load_file(dest)


def test_load_4(monkeypatch, tmp_path):
    """unittest for pickle_dml.load: wrong Application option
    """
    dest = tmp_path / 'load4.pck'
    dest.touch()
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {0: {'Application': 'x'}})
    with pytest.raises(EOFError):
        dmlp.load_file(dest)


def test_load_5(monkeypatch, tmp_path):
    """unittest for pickle_dml.load: no errors
    """
    dest = tmp_path / 'load5.pck'
    dest.touch()
    conf = {'Application': 'NoteTree', 'ScreenSize': (9, 6), 'Selection': [10, 1],
            'SashPosition': [55]}
    monkeypatch.setattr(dmlp.pck, 'load', lambda x: {0: conf, '01-01-0001 00:00:00': 'x'})
    assert dmlp.load_file(dest) == {0: {'Application': 'NoteTree', 'ScreenSize': (9, 6),
                                    'Selection': (10,1), 'SashPosition': (55,)},
                                    '01-01-0001 00:00:00': 'x'}  # is dit alleen text, geen keywords?


def test_save(monkeypatch, capsys, tmp_path):
    """unittest for pickle_dml.save
    """
    def mock_save(*args, **kwargs):
        """stub
        """
        print(f'called pickle.dump for data `{args[0]}`')
    dest = tmp_path / 'save.pck'
    data = 'nt_data'
    monkeypatch.setattr(dmlp.pck, 'dump', mock_save)
    dmlp.save_file(dest, data)
    assert capsys.readouterr().out == 'called pickle.dump for data `nt_data`\n'
