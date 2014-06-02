# This Test opens a simple pdb file (data/init_pdbs/pr/1mui_wat.pdb)
# It then attempts to manipulate this file using MDAnalyis.

import MDAnalysis

data_dir = "../data"

def test_load_pdb_file():
  from pdb_io import load_pdb
  load_pdb("%s/init_pdbs/pr/1mui_wat.pdb" % data_dir)
  #universe = Universe(topology, trajectory)
  print "PDB file loaded!"

def test_print_pdb_file():
  from pdb_io import print_pdb
  print_pdb("%s/init_pdbs/pr/1mui_wat.pdb" % data_dir)
