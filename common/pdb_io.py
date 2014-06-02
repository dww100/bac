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


def write_pdb_file(u, filename):
  u.write(filename)


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


def select_atoms_by_name(selection, resname, names):
  """ Delete atoms by name in a residue. if resname == "-1" then the atoms are
  deleted from all residues.
  """
  assert len(selection) > 0

  news = selection.selectAtoms("not all") #'not all' means NONE in MDAnalysis ;).

  if(type(names) == str):
    if resname != "-1":
      for a in selection:
        if a.resname == resname:
          if a.name == names:
            news += a
        else:
          news += a
    else:
      for a in selection:
        if a.name == names:
          news += a
  if(type(names) == list):
    if resname != "-1":
      for a in selection:
        if a.resname == resname:
          if a.name in names:
            news += a
        else:
          news += a
    else:
      for a in selection:
        if a.name in names:
          news += a

  return news
 

def mutate_residue(atomgroup, resname, new_residue_name=''):
  if resname == new_residue_name:
    return atomgroup

  atomgroup = select_atoms_by_name(atomgroup, resname, ["C", "CA", "N", "O", "CB"]) 
  for t in atomgroup:
    t.resname = new_residue_name
  return atomgroup
