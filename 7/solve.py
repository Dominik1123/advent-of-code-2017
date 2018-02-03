from collections import defaultdict
import re

import numpy as np


def parse_program(p):
    """
    Returns tuple (name, weight, children[list]).
    """
    match = re.match(r'^(?P<name>[a-z]+) \((?P<weight>\d+)\)( -> (?P<children>[a-z,\s]+))?$',
                     p.strip())
    name = match.groupdict()['name']
    weight = int(match.groupdict()['weight'])
    children = match.groupdict()['children'].replace(' ', '').split(',') \
        if match.groupdict()['children'] is not None else []
    return name, weight, children


with open('input.txt') as fp:
    programs = list(map(parse_program, fp))


def tree():
    return defaultdict(tree)

root = tree()
# Store all programs that are already part of the tree together with the path to their node.
# program_name -> list_of_parent_names
connected = {}


def get_node(start, path):
    if len(path) == 1:
        return start[path[0]]
    return get_node(start[path[0]], path[1:])


def branch_up(name, path=()):
    global root
    global connected

    def _connect_nodes(anchor):
        node = anchor
        for i, leaf in enumerate(path):
            node = node[leaf]
            connected[leaf] = connected[name] + path[:i+1]

    # If this node is already part of the tree, then connect all its children as well.
    if name in connected:
        _connect_nodes(get_node(root, connected[name]))
        return

    try:
        parent = next(filter(lambda x: name in x[2], programs))[0]
    except StopIteration:
        # This node does not have a parent, i.e. it must be the root node. Connect it and all its
        # children to the tree.
        connected[name] = (name,)
        _connect_nodes(root[name])
        return
    else:
        branch_up(parent, (name,) + path)


leafs = filter(lambda x: not x[2], programs)
for leaf in leafs:
    branch_up(leaf[0])

assert len(root.keys()) == 1, 'Multiple root programs found'
root_program = list(root.keys())[0]
print('Root: {}'.format(root_program))

weights = dict(map(lambda x: x[:2], programs))


def compute_sub_weights(start, name):
    global weights

    children = list(start.keys())
    if children:
        sub_weights = np.asarray(
            list(map(lambda x: compute_sub_weights(start[x], x),
                     children)),
            dtype=int
        )
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
                  .format(which, weights[which], adjust_by, weights[which] + adjust_by))
        return np.sum(sub_weights) + weights[name]
    else:
        return weights[name]

# The first program that is printed is the one that needs to be balanced because its location is
# the deepest within the tree.
compute_sub_weights(root[root_program], root_program)
