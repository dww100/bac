# This Test opens a simple pdb file (data/init_pdbs/pr/1mui_wat.pdb)
# It then attempts to manipulate this file using MDAnalyis.

from pdb_io import *
from operator import itemgetter, attrgetter
from nose.tools import assert_equals


def test_mutation():
  u = load_pdb("../data/minimal_test.pdb")
  s = u.selectAtoms("all")
  s = mutate_residue(s, 'PRO', new_residue_name='ALA')
  write_pdb_file(s, "test.pdb")
