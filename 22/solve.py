from collections import defaultdict
import numpy as np


grid = defaultdict(bool)

with open('input.txt') as fp:
    for y, row in enumerate(fp):
        for x, node in enumerate(row.strip()):
            grid[y, x] = node == '#'

turn_right = np.asarray([[0, 1], [-1, 0]])
turn_left = np.asarray([[0, -1], [1, 0]])


def burst(yx, d_yx):
    """
    Returns updated position yx, updated velocity d_yx and whether the current has been infected:
    (yx, d_yx, infected)
    """
    node = grid[tuple(yx)]
    grid[tuple(yx)] = not node
    d_yx = turn_right @ d_yx if node else turn_left @ d_yx
    return yx + d_yx, d_yx, not node


infections = 0
yx = np.asarray([y+1, x+1]) // 2
d_yx = np.asarray([-1, 0])
for i_burst in range(10000):
    yx, d_yx, infected = burst(yx, d_yx)
    infections += infected

print('Number of new infections: ', infections)
