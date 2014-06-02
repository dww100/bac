from common.io_pdb import *

def mutate_residue(atomgroup, resname, new_residue_name=''):
  if resname == new_residue_name:
    return atomgroup

  atomgroup = select_atoms_by_name(atomgroup, resname, ["C", "CA", "N", "O", "CB"])
  for t in atomgroup:
    t.resname = new_residue_name
  return atomgroup

