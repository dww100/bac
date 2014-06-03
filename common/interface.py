# -*- coding: utf-8 -*-
import yaml
"""

"""

aa1to3 = {
'A':'ALA',
'C':'CYS',
'D':'ASP',
'E':'GLU',
'H':'HIS',
'I':'ILE',
'K':'LYS',
'L':'LEU',
'M':'MET',
'N':'ASN',
'P':'PRO',
'Q':'GLN',
'R':'ARG',
'S':'SER',
'T':'THR',
'V':'VAL',
'W':'TRP',
'Y':'TYR'
}

def collate_mutation_dict(mutation_dict):
    """ This function merges multiple mutations on one residue into a single 
        combined mutation.
    """
    out_dict = {}
    for residue_key in mutation_dict:
        out_dict[residue_key] = mutation_dict[residue_key][0][0] +  mutation_dict[residue_key][-1][-1]

    return out_dict


def write_mutation_to_yaml(mutation_list, filename):
    """ This function converts a mutation list to a dict and writes it to 
        a yaml file.
    """
    mutation_dict = {}
    for m in mutation_list:
        if not m[1:3] in mutation_dict:
            mutation_dict[m[1:-1]] = [m[0:1]+m[-1:]]
        else:
            mutation_dict[m[1:-1]].append(m[0:1]+m[-1])

    outfile = open(filename, 'w')
    outfile.write(yaml.dump(mutation_dict))

