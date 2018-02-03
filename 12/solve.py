import re
import numpy as np


def parse(s):
    match = re.match(r'^(\d+) <-> ([\d\s,]+)$', s.strip())
    return int(match.groups()[0]), list(map(int, match.groups()[1].split(',')))


with open('input.txt') as fp:
    programs = list(map(parse, fp))

pipes = np.zeros([len(programs)]*2, dtype=bool)

for program, speaks_to in programs:
    for partner in speaks_to:
        pipes[program, partner] = True
        pipes[partner, program] = True

# import scipy.sparse.csgraph as csgraph
# graph = csgraph.csgraph_from_dense(pipes)
# print(csgraph.connected_components(graph, return_labels=False))

group = np.array((0,), dtype=int)


def traverse(index):
    global group

    connections = np.argwhere(pipes[index])
    new_connections = connections[~np.isin(connections, group)]
    group = np.append(group, new_connections)
    for new in new_connections:
        traverse(new)

traverse(0)
print('Number of programs in group: ', group.size)


# Part 2.

in_group = np.zeros(pipes.shape[0], dtype=bool)
in_group[group] = True
n_groups = 1

while in_group.sum() < in_group.size:
    start = np.argwhere(~in_group)[0]
    group = np.array((start,), dtype=int)
    traverse(start)
    in_group[group] = True
    n_groups += 1

print('Number of groups: ', n_groups)
