"""test of de verschillende backends uitwisselbaar zijn

1. laad een datafile met een gegeven backend en pprint de geladen structuur
2. schrijf het weg met hetzelfde backend, laad nogmaals en pprint weer
3. schrijf het weg met een ander backend en herhaal stappen 1 en 2

4. vergelijk de uitkomsten van 1 en 2  en van 1 en 3

"""
import subprocess
import pprint
import notetree.pickle_dml as dmlp
import notetree.sql_dml as dmls
import notetree.json_dml as dmlj

p_filename = 'MyNotes.pck'
s_filename = p_filename.replace('.pck', '.db')
j_filename = p_filename.replace('.pck', '.json')

nt_data = dmlp.load_file(p_filename)
with open(p_filename + '.out-loaded', 'w') as out:
    pprint.pprint(nt_data, stream=out)
dmlp.save_file(p_filename, nt_data)
nt_data = dmlp.load_file(p_filename)
with open(p_filename + '.out-saved', 'w') as out:
    pprint.pprint(nt_data, stream=out)

dmls.save_file(s_filename, nt_data)
new_data = dmls.load_file(s_filename)
with open(s_filename + '.out-loaded', 'w') as out:
    pprint.pprint(new_data, stream=out)
dmls.save_file(s_filename, new_data)
new_data = dmls.load_file(s_filename)
with open(s_filename + '.out-saved', 'w') as out:
    pprint.pprint(new_data, stream=out)

dmlj.save_file(j_filename, nt_data)
new_data = dmlj.load_file(j_filename)
with open(j_filename + '.out-loaded', 'w') as out:
    pprint.pprint(new_data, stream=out)
dmlj.save_file(j_filename, new_data)
new_data = dmlj.load_file(j_filename)
with open(j_filename + '.out-saved', 'w') as out:
    pprint.pprint(new_data, stream=out)

print('comparing pickle save and load')
subprocess.run(['diff', '{}.out-loaded'.format(p_filename), '{}.out-saved'.format(p_filename)])
print('comparing pickle load and sql save')
# hier verschillen vanwege gebruik lists ipv tuples
subprocess.run(['diff', '{}.out-loaded'.format(p_filename), '{}.out-saved'.format(s_filename)])
print('comparing sql save and load')
subprocess.run(['diff', '{}.out-loaded'.format(s_filename), '{}.out-saved'.format(s_filename)])
print('comparing sql load and json save')
# hier verschil vanwege ontbreken keywords in één van beide
subprocess.run(['diff', '{}.out-loaded'.format(s_filename), '{}.out-saved'.format(j_filename)])
print('comparing json save and load')
subprocess.run(['diff', '{}.out-loaded'.format(j_filename), '{}.out-saved'.format(j_filename)])
