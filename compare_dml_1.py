"""test of de verschillende formats hetzelfde opleveren

1. simuleer aanmaken van datafile zonder de gui (voor elk backend)
2. laad met het betreffende backend en print de datastructuur
3. vergelijk de 3 prints
"""
import subprocess
import pathlib
import notetree.pickle_dml as dmlp
import notetree.sql_dml as dmls
import notetree.json_dml as dmlj
from notetree.settings import backend

settingsfile = pathlib.Path('notetree/settings.py')
backend_types = ['pck', 'json', 'sql'] * 2
def next_backend(fromvalue, tovalue):
    data = settingsfile.read_text()
    old = "backend = '{}'".format(backend_types[fromvalue])
    new = "backend = '{}'".format(backend_types[tovalue])
    data = data.replace(old, new)
    settingsfile.write_text(data)

def test_main():
    startdir = pathlib.Path('/tmp/notetree')
    startdir.mkdir(exist_ok=True)
    for path in startdir.iterdir():
        (startdir / path).unlink()
    filename = startdir / 'testdata'

    startvalue = backend_types.index(backend)
    for count in range(3):
        subprocess.run(['pytest', 'sample.py'])
        next_backend(startvalue, startvalue + 1)
        startvalue += 1

    p_filename = str(filename.with_suffix('.pck'))
    pck_data = dmlp.load_file(p_filename)
    with open(p_filename + '.out', 'w') as out:
    #     pprint.pprint(pck_data, stream=out)
        for key, value in pck_data.items():
            print(key, value, file=out)

    s_filename = str(filename.with_suffix('.db'))
    sql_data = dmls.load_file(s_filename)
    with open(s_filename + '.out', 'w') as out:
    #     pprint.pprint(sql_data, stream=out)
        for key, value in sql_data.items():
            print(key, value, file=out)

    j_filename = str(filename.with_suffix('.json'))
    json_data = dmlj.load_file(j_filename)
    with open(j_filename + '.out', 'w') as out:
    #     pprint.pprint(json_data, stream=out)
        for key, value in json_data.items():
            print(key, value, file=out)

    subprocess.run(['meld', p_filename + '.out', s_filename + '.out', j_filename + '.out'])

if __name__ == '__main__':
    test_main()
