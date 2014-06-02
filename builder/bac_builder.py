from common.pdb_io import *
import subprocess

def mutate_residue(atomgroup, resname, new_residue_name=''):
  """
  Mutates the residue(s) into new_residue_name. The only atoms retained are
  the backbone and CB. If esname == new_residue_name the residue is left 
  untouched.
  """    
    
  if resname == new_residue_name:
    return atomgroup

  atomgroup = select_atoms_by_name(atomgroup, resname, ["C", "CA", "N", "O", "CB"])
  for t in atomgroup:
    if t.resname == resname:
      t.resname = new_residue_name
  return atomgroup

def edit_leap_input(specification, filename):
    """
    Read in the template Leap input file and replace variables (specified with 
    a leading $ character) with appropriate values from the input specification
    dictionary. This is output to the specified file.)
    """
    
    template = 'tleap_template.txt'

    out_file = open(filename, 'w')    
    
    with open(template, 'r') as f:
        for line in f:
            for var_name, value in specification.items():
                line = line.replace('$%s' % var_name, value)
            out_file.write(line)
            
    out_file.close()
    
    return

def amber_parameterize(specification):
    """
    Edit the Leap input to reflect the input specification dictionary and run 
    tLeap to create completed PDB and topology files for the complex (both 
    prior to and after solvation), the receptor and the ligand.
    """

    leap_input = specification['TARGET_DIR'] + '/leap.in'

    edit_leap_input(specification, leap_input)
    
    result = subprocess.check_output(['tleap','-f', leap_input], stderr=subprocess.STDOUT)

    return

        