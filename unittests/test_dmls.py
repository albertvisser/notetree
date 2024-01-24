"""unittests for ./notetree/sql_dml.py
"""
import json
import pytest
import notetree.sql_dml as dmls


class MockConn:
    """stub for sqlite3.Connection
    """
    def cursor(self, *args, **kwargs):
        """stub
        """
        return MockCursor()
    def commit(self, *args, **kwargs):
        """stub
        """
        print('called commit() on connection')
    def close(self, *args):
        """stub, needed for context handler
        """


class MockCursor:
    """stub for sqlite3.Cursor
    """
    lastrowid = 0
    def __iter__(self):
        """stub
        """
    def execute(self, *args):
        """stub
        """
        print(f'execute SQL: `{args[0]}`')
        if len(args) > 1:
            print('  with:', ', '.join([f'`{x}`' for x in args[1]]))
    def executemany(self, *args):
        """stub
        """
        print(f'execute SQL: `{args[0]}`')
        if len(args) > 1:
            print('  with:', ', '.join([f'`{x}`' for x in args[1]]))
    def executescript(self, *args):
        """stub
        """
        print(f'execute SQL: `{args[0]}`')
    def commit(self, *args, **kwargs):
        """stub
        """
        print('called commit() on cursor')
    def close(self, *args, **kwargs):
        """stub
        """
        print('called close()')
    def fetchone(self, *args, **kwargs):
        """stub
        """
    def fetchall(self, *args, **kwargs):
        """stub
        """


def test_load_1(capsys, tmp_path):
    """unittest for sql_dml.load: file does not exist
    """
    dest = tmp_path / 'load1.sql'
    dest.unlink(missing_ok=True)
    assert dmls.load_file(dest) == {}
    assert capsys.readouterr().out == ''


def test_load_2(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.load: file exists but missing Application option
    """
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    def mock_iter(*args):
        """stub
        """
        return (x for x in [('1', '01-01-0001 00:00:00', 'title_1', 'text_1')])
    dest = tmp_path / 'load2.sql'
    dest.touch()
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    monkeypatch.setattr(MockCursor, '__iter__', mock_iter)
    with pytest.raises(EOFError):
        dmls.load_file(dest)
    assert capsys.readouterr().out == ('execute SQL:'
                                       ' `SELECT noteid, created, title, text FROM notes`\n')


def test_load_3(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.load: wrong Application option
    """
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    def mock_iter(*args):
        """stub
        """
        return (x for x in [(0, '', '', '{"Application": "x"}'),
                            (1, '01-01-0001 00:00:00', 'title_1', 'text_1')])
    dest = tmp_path / 'load3.sql'
    dest.touch()
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    monkeypatch.setattr(MockCursor, '__iter__', mock_iter)
    with pytest.raises(EOFError):
        dmls.load_file(dest)
    assert capsys.readouterr().out == ('execute SQL:'
                                       ' `SELECT noteid, created, title, text FROM notes`\n')


def test_load_4(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.load: everyting ok, no tags
    """
    conf = {"Application": 'NoteTree', "ScreenSize": (9, 6), "Selection": [10, 1],
            "SashPosition": [55]}
    count = 0
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    def mock_iter(*args):
        """stub
        """
        nonlocal count
        count += 1
        if count == 1:
            return (x for x in [(0, '', '', json.dumps(conf)),
                                (1, '01-01-0001 00:00:00', 'title_1', 'text_1')])
        return (x for x in [])
    dest = tmp_path / 'load4.sql'
    dest.touch()
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    monkeypatch.setattr(MockCursor, '__iter__', mock_iter)
    # assert dmls.load_file(dest) == {0: {'Application': 'NoteTree', 'Keywords': []},
    assert dmls.load_file(dest) == {0: {'Application': 'NoteTree', 'ScreenSize': (9, 6),
                                        'Selection': (10,1), 'SashPosition': (55,), 'Keywords': []},
                                    '01-01-0001 00:00:00': ('title_1', 'text_1', [])}
    assert capsys.readouterr().out == ('execute SQL:'
                                       ' `SELECT noteid, created, title, text FROM notes`\n'
                                       'execute SQL: `SELECT tagid, tagname FROM tags`\n'
                                       'execute SQL: `SELECT doc_id, tag_id FROM links`\n')


def test_load_5(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.load: everyting ok, with tags
    """
    conf = {'Application': 'NoteTree', 'ScreenSize': (9, 6), 'Selection': [10, 1],
            'SashPosition': [55]}
    count = 0
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    def mock_iter(*args):
        """stub
        """
        nonlocal count
        count += 1
        if count == 1:
            return (x for x in [(0, '', '', json.dumps(conf)),
                                (1, '01-01-0001 00:00:00', 'title_1', 'text_1')])
        if count == 2:
            return (x for x in [('tagid_1', 'tag_title_1')])
        # if count == 3:
        return (x for x in [(1, 'tagid_1')])
    dest = tmp_path / 'load5.sql'
    dest.touch()
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    monkeypatch.setattr(MockCursor, '__iter__', mock_iter)
    # assert dmls.load_file(dest) == {0: {'Application': 'NoteTree', 'Keywords': ['tag_title_1']},
    assert dmls.load_file(dest) == {0: {'Application': 'NoteTree', 'ScreenSize': (9, 6),
                                        'Selection': (10,1), 'SashPosition': (55,),
                                        'Keywords': ['tag_title_1']},
                                    '01-01-0001 00:00:00': ('title_1', 'text_1', ['tag_title_1'])}
    assert capsys.readouterr().out == ('execute SQL:'
                                       ' `SELECT noteid, created, title, text FROM notes`\n'
                                       'execute SQL: `SELECT tagid, tagname FROM tags`\n'
                                       'execute SQL: `SELECT doc_id, tag_id FROM links`\n')


def test_save_1(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.save: nt_data is empty (is this possible?)
    """
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    dest = tmp_path / 'save1.sql'
    data = {}
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    dmls.save_file(dest, data)
    assert capsys.readouterr().out == (f'execute SQL: `{dmls.init_db}`\n'
                                       'called commit() on connection\n')


def test_save_2(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.save: nt_data has no item with created = 0 (also not possible?)
    """
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    dest = tmp_path / 'save2.sql'
    data = {'01-01-0001 00:00:00': ('title', 'text', ['keyword'])}
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    dmls.save_file(dest, data)
    assert capsys.readouterr().out == (f'execute SQL: `{dmls.init_db}`\n'
                                       'execute SQL: `INSERT INTO notes (noteid, created,'
                                       ' title, text) VALUES(?, ?, ?, ?)`\n'
                                       '  with: `1`, `01-01-0001 00:00:00`, `title`, `text`\n'
                                       'called commit() on connection\n')
    # note that without the 0 key, no associated keywords are saved. Luckily this is not realistic


def test_save_3(monkeypatch, capsys, tmp_path):
    """unittest for sql_dml.save: nt_data is complete
    """
    def mock_connect(*args):
        """stub
        """
        return MockConn()
    dest = tmp_path / 'save2.sql'
    data = {0: {'Application': 'NoteTree', 'Keywords': ['keyword']},
            '01-01-0001 00:00:00': ('title', 'text', ['keyword'])}
    monkeypatch.setattr(dmls.sql, 'connect', mock_connect)
    dmls.save_file(dest, data)
    assert capsys.readouterr().out == (f'execute SQL: `{dmls.init_db}`\n'
                                       'execute SQL: `INSERT INTO notes (noteid, created,'
                                       ' title, text) VALUES(?, ?, ?, ?)`\n'
                                       '  with: `0`, ``, ``, `{"Application": "NoteTree"}`\n'
                                       'execute SQL: `INSERT INTO notes (noteid, created,'
                                       ' title, text) VALUES(?, ?, ?, ?)`\n'
                                       '  with: `1`, `01-01-0001 00:00:00`, `title`, `text`\n'
                                       'execute SQL: `INSERT INTO tags (tagid, tagname)'
                                       ' VALUES(?, ?)`\n'
                                       "  with: `(0, 'keyword')`\n"
                                       'execute SQL: `INSERT INTO links (doc_id, tag_id)'
                                       ' VALUES(?, ?)`\n'
                                       "  with: `(0, 0)`\n"
                                       'called commit() on connection\n')
