import MDAnalysis as mda

def load_pdb(filename):
  u = mda.Universe(filename) 
  # use PDB file in one arg mode, applying it both as 'topology' 
  # and as 'trajectory' input.
  return u

def print_pdb(filename):
  u = load_pdb(filename)
  print u.atoms
  print u.trajectory
