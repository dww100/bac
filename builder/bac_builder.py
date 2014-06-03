from common.pdb_io import *
import subprocess


def mutate_residue(atomgroup, resnum, new_residue_name, segid = None):

    unchanged = select_atoms(atomgroup, "not all")    
    
    if segid:
        select_text = "segid " + segid + " and resnum " + str(resnum)
        unchanged += select_atoms(atomgroup, "not (" + select_text + ")")
        target = select_atoms(atomgroup, select_text)
    else:
        select_text = "resnum " + str(resnum)
        unchanged += select_atoms(atomgroup, "not (" + select_text + ")")
        target = select_atoms(atomgroup, select_text)

    mutations = select_atoms(atomgroup, "not all") 
    for resid in target.residues:
        mutations += mutate_single_residue(resid, new_residue_name)
    
    mutated = merge_atom_selections([unchanged, mutations])
    
    return mutated
    
def mutate_single_residue(atomgroup, new_residue_name):
    """
    Mutates the residue(s) into new_residue_name. The only atoms retained are
    the backbone and CB. If esname == new_residue_name the residue is left 
    untouched.
    """    

    resnames = atomgroup.resnames()

    if len(resnames) == 1:
        if resnames[0] == new_residue_name:
            edited_atomgroup = atomgroup
        else:
            edited_atomgroup = select_atoms_by_name(atomgroup, ["C", "CA", "N", "O", "CB"])
            for t in edited_atomgroup:
                t.resname = new_residue_name
    else:
        edited_atomgroup = atomgroup
                    
    return edited_atomgroup

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

def chains_selection(chains):
    select_text = ''
    for chain in chains:
        if len(select_text) > 0:
            select_text += ' or segid ' + chain
        else:
            select_text += 'segid ' + chain
    return select_text

def split_pdb_chains(strucure, rec_chains, lig_chains, sol_chains):

    select_rec = chains_selection(rec_chains)    
    rec = select_atoms(structure, select_rec)

    select_lig = chains_selection(lig_chains)    
    lig = select_atoms(structure, select_lig)    

    select_sol = chains_selection(lig_chains)    
    sol = select_atoms(structure, select_lig)
    
    return rec, lig, sol
    
