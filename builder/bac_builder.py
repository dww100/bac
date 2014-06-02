from common.pdb_io import *

def mutate_residue(atomgroup, resname, new_residue_name=''):
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

    with open(template, 'r') as f:
        temp_text = f.read()

    f = open(filename, 'w')    
    
    for line in temp_text:
        # Perform variable substitution on each line        
        for var_name, value in specification.items():
            out_line = line.replace('$%s' % var_name, value)
            f.write(line)
            
    f.close()
    
    return
        