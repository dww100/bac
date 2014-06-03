# This Test opens a simple pdb file (data/init_pdbs/pr/1mui_wat.pdb)
# It then attempts to manipulate this file using MDAnalyis.

from common.pdb_io import *
from bac_builder import *
from operator import itemgetter, attrgetter
from nose.tools import assert_equals


#def test_mutation_all():
#  u = load_pdb("../data/minimal_test.pdb")
#  s = u.selectAtoms("all")
#  s = mutate_residue(s, 'PRO', new_residue_name='ALA')
#  write_pdb_file(s, "test.pdb")


#def test_mutation_pro():
#  u = load_pdb("../data/minimal_test.pdb")
#  s = u.selectAtoms("resname PRO")
#  s = mutate_residue(s, 'PRO', new_residue_name='ALA')
#  assert_equals(len(s), 1)

def test_mutation_1mui_wat():
  u = load_pdb("../data/init_pdbs/pr/1mui_wat.pdb")
  ab = u.selectAtoms("segid A or segid B")
  x = u.selectAtoms("segid X")
  s = u.selectAtoms("segid S")
 
  ab = mutate_residue(ab, 1, 'PRO', 'ALA', segid = 'A')
  assert_equals(len(ab)+len(s)+len(x), 1514) #1mui_wat.pdb has 1514 atoms, all of them should have been selected.

  write_pdb_file(ab, "ab.pdb")
  write_pdb_file(x, "x.pdb")
  write_pdb_file(s, "s.pdb")

def test_amber_parameterize():
  
  specification = {
      'TARGET_DIR':'../test/',
      'FF':'leaprc.ff03.r1',
      'FRCMOD':'../data/amber/drugs/pr/resp/lpv/lpv.frcmod',
      'PREP':'../data/amber/drugs/pr/resp/lpv/lpv.prep',
      'LIGAND_PDB':'../data/test_lig.pdb',
      'RECEPTOR_PDB':'../data/test_rec.pdb',
      'SOLVENT_PDB':'../data/test_sol.pdb',
      'WATERBOX':'14 iso'
  }
  
  amber_parameterize(specification)