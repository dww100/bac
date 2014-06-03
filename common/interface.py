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
    for chain_key, chain_dict in mutation_dict.iteritems():
        for residue_key, residue_mutations in chain_dict.iteritems():

            # Sanity test prior to merging the mutations on one residue. 
            if type(residue_mutations) != str and len(residue_mutations) > 1:
                for i in range(1, len(residue_mutations)):
                    if residue_mutations[i-1][1] != residue_mutations[i][0]:
                        print "Error: inconsistent mutation list in: ", residue_key, residue_mutations
                        print "This mutation would never completely occur."
                        raise StandardError

            out_dict[residue_key] = residue_mutations[0][0] +  residue_mutations[-1][-1]
    return out_dict


def write_mutation_to_yaml(mutation_list, filename):
    """ This function converts a mutation list to a dict and writes it to 
        a yaml file.
    """
    mutation_dict = {}
    chain_dict = {}
    for m in mutation_list:
        if len(m) == 1: # Field indicates a single letter (chain)
            mutation_dict[m] = {}
            chain_dict = mutation_dict[m]
        else: # Letter-Number-Letter field indicates mutation in the current chain.
            if not m[1:3] in chain_dict:
                chain_dict[m[1:-1]] = [m[0:1]+m[-1:]]
            else:
                chain_dict[m[1:-1]].append(m[0:1]+m[-1])

    outfile = open(filename, 'w')
    outfile.write(yaml.dump(mutation_dict))

