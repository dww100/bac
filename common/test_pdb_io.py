# This Test opens a simple pdb file (data/init_pdbs/pr/1mui_wat.pdb)
# It then attempts to manipulate this file using MDAnalyis.

from pdb_io import *
from operator import itemgetter, attrgetter
from nose.tools import assert_equals

data_dir = "../data"


def test_load_pdb_file():
  load_pdb("%s/init_pdbs/pr/1mui_wat.pdb" % data_dir)
  #universe = Universe(topology, trajectory)
  print "PDB file loaded!"

def test_print_pdb_file():
  print_pdb_file("%s/init_pdbs/pr/1mui_wat.pdb" % data_dir)

def test_pdb_select_and_merge():
  u = load_pdb("%s/init_pdbs/pr/1mui_wat.pdb" % data_dir)
  target = select_atoms(u, "segid A")
  s1 = select_atoms(u, "segid A and resnum 10")
  s2 = select_atoms(u, "segid A and not resnum 10")
  s3 = s2 + s1 
  #if s3 is sorted properly, then the last element should be s2[-1]
  s4 = sort_atom_selection(s3)
  assert_equals(s2[-1].number, s4[-1].number)
  s5 = merge_atom_selections([s2,s1])
  assert_equals(s2[-1].number, s5[-1].number)
