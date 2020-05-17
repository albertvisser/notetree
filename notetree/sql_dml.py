"""Notetree data benadering via sql(ite)
"""
import os.path
import contextlib
import datetime
import collections
import json
import sqlite3 as sql
init_db = """\
DROP TABLE IF EXISTS notes;
CREATE TABLE notes (noteid  INTEGER PRIMARY KEY,
                    created STRING,
                    title   STRING,
                    text    TEXT);
DROP TABLE IF EXISTS tags;
CREATE TABLE tags (tagid   INTEGER PRIMARY KEY,
                   tagname STRING);
DROP TABLE IF EXISTS links;
CREATE TABLE links (doc_id INTEGER REFERENCES notes(noteid),
                    tag_id INTEGER REFERENCES tags(tagid));
CREATE INDEX IF NOT EXISTS linksbydoc ON links(doc_id);
CREATE INDEX IF NOT EXISTS linksbytag ON links(tag_id);
"""
insert_note = 'INSERT INTO notes (noteid, created, title, text) VALUES(?, ?, ?, ?)'
insert_tag ='INSERT INTO tags (tagid, tagname) VALUES(?, ?)'
insert_link = 'INSERT INTO links (doc_id, tag_id) VALUES(?, ?)'
read_notes = 'SELECT noteid, created, title, text FROM notes'
read_tags  = 'SELECT tagid, tagname FROM tags'
read_links = 'SELECT doc_id, tag_id FROM links'


def load_file(filename):
    """raise EOFError als file niet gelezen kan worden
    geeft geen resultaat als bestand niet bestaat
    """
    if not os.path.exists(filename):
        return {}
    nt_data, docdict = {}, {}
    with contextlib.closing(sql.connect(filename)) as db:
        cur = db.cursor()
        cur.execute(read_notes)
        for line in cur:
            noteid, created, title, text = line
            if noteid == 0:
                nt_data[0] = json.loads(text)
            elif noteid == 1:
                nt_data[0][title] = text
            else:
                nt_data[created] = [title, text, []]
                docdict[noteid] = created
        cur.execute(read_tags)
        tagdict = {x: y for (x, y) in cur}
        nt_data[0]['Keywords'] = list(tagdict.values())
        cur.execute(read_links)
        for line in cur:
            doc_id, tag_id = line
            nt_data[docdict[doc_id]][2].append(tagdict[tag_id])
        settings = nt_data.pop(0)
        ordered = collections.OrderedDict()
        ordered[0] = settings
        for key in sorted(nt_data.keys(),
                          key=lambda x: datetime.datetime.strptime(x, "%d-%m-%Y %H:%M:%S")):
            ordered[key] = nt_data[key]
    return ordered


def save_file(filename, nt_data):
    """simple overwrite; backup should be done by the calling program (or not)
    """
    with contextlib.closing(sql.connect(filename)) as db:
        cur = db.cursor()
        cur.executescript(init_db)
        count = 0
        settings = nt_data.pop(0)
        keywords = [x for x in settings.pop('Keywords')]
        sashposition = settings.pop('SashPosition')
        # de rest van de settings serializen naar een json string in plaats van apart opslaan
        # en deze in de eerste note entry opslaan
        cur.execute(insert_note, (0, '', '', json.dumps(settings)))
        cur.execute(insert_note, (1, '', 'SashPosition', sashposition))
        tagdict = collections.defaultdict(list)
        count = 1
        for created, value in nt_data.items():
            title, text, tags = value
            count += 1
            cur.execute(insert_note, (count, created, title, text))
            doc_id = cur.lastrowid
            for tag in tags:
                tagdict[tag].append(doc_id)
        cur.executemany(insert_tag, enumerate(keywords))
        for ix, word in enumerate(keywords):
            docs = [(x, ix) for x in tagdict[word]]
            cur.executemany(insert_link, docs)
        db.commit()
