import MDAnalysis as mda
from operator import attrgetter

def load_pdb(filename):
  u = mda.Universe(filename) 
  # use PDB file in one arg mode, applying it both as 'topology' 
  # and as 'trajectory' input.
  return u

def print_pdb_file(filename):
  u = load_pdb(filename)
  print_pdb(u)

def print_pdb(u):
  print u.atoms
  print u.trajectory

def select_atoms(u, select_condition):
  return u.selectAtoms(select_condition)

def sort_atom_selection(selection):
  return sorted(selection, key=attrgetter('number'))

def merge_atom_selections(selections):
  assert len(selections) > 1
  
  out = selections[0]   
  for s in selections[1:]:
    out += s

  return sort_atom_selection(out)  
