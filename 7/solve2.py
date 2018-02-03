import re

import numpy as np


# Find root element.
# The root element's name is the only one that occurs only once in the input file
# as it is not part of any children list.
with open('input.txt') as fp:
    names, counts = np.unique(np.asarray(re.findall(r'[a-z]+', fp.read())), return_counts=True)
    print('Root: {}'.format(names[counts == 1]))
    assert np.sum(counts == 1) == 1, 'Multiple root elements found'
    root = names[counts == 1][0]


def parse_program(p):
    """
    Returns tuple (name, (weight, children[list])).
    """
    match = re.match(r'^(?P<name>[a-z]+) \((?P<weight>\d+)\)( -> (?P<children>[a-z,\s]+))?$',
                     p.strip())
    name = match.groupdict()['name']
    weight = int(match.groupdict()['weight'])
    children = match.groupdict()['children'].replace(' ', '').split(',') \
        if match.groupdict()['children'] is not None else []
    return name, (weight, children)


with open('input.txt') as fp:
    programs = dict(map(parse_program, fp))


def compute_sub_weights(name):
    global programs

    children = programs[name][1]
    sub_weights = np.asarray(list(map(compute_sub_weights, children)), dtype=int)
    unique_weights, counts = np.unique(sub_weights, return_counts=True)

    if unique_weights.size > 1:
        invalid = unique_weights[counts == 1][0]
        valid = unique_weights[counts > 1][0]
        adjust_by = valid - invalid
        which = children[np.argwhere(sub_weights == invalid).flatten()[0]]
        print('{}\' disc is not balanced: {}'.format(name, sub_weights.tolist()))
        print('Involves programs: {}'.format(children))
        print('{} is too {}'.format(which, 'heavy' if adjust_by < 0 else 'light'))
        print('Adjust {}\'s weight ({}) by {} -> {}'
              .format(which, programs[which][0], adjust_by, programs[which][0] + adjust_by))
    return np.sum(sub_weights) + programs[name][0]

# The first program that is printed is the one that needs to be balanced because its location is
# the deepest within the tree.
compute_sub_weights(root)
