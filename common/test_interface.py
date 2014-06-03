from interface import *
from nose.tools import assert_equals

def test_write_mutation_to_yaml():
    data = []
    data.append("A")
    data.append("M10N")
    data.append("P13L")
    data.append("N10P")
    data.append("K9M")
    data.append("B")
    data.append("C23K")
    data.append("N10P")

    write_mutation_to_yaml(data, 'test.yml')



def test_collate_mutation_dict():
    data = {'A': {1: ['MN'], 4:['OK','KA'], 8:['CH']}}
    data = collate_mutation_dict(data)
    
    assert_equals(type(data[1]), str)
    assert_equals(len(data), 3)
    assert_equals(len(data[1]), 2)

    wrong_data = {'A': {1: ['MN'], 4:['OM','KA'], 8:['CH']}}
    try:
        wrong_data = collate_mutation_dict(wrong_data)
    except StandardError:
        assert(True)
    else:
        assert(False)
