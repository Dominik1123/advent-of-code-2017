from collections import defaultdict
import numpy as np


# 0: clean, 1: weakened, 2: infected, 3: flagged.
grid = defaultdict(int)

with open('input.txt') as fp:
    for y, row in enumerate(fp):
        for x, node in enumerate(row.strip()):
            grid[y, x] = 2 if node == '#' else 0

turn_right = np.asarray([[0, 1], [-1, 0]])
turns = {
    # Turn left = turn right three times.
    0: turn_right @ turn_right @ turn_right,
    1: np.identity(2, dtype=int),
    2: turn_right,
    3: turn_right @ turn_right,
}


def burst(yx, d_yx):
    """
    Returns updated position yx, updated velocity d_yx and whether the current has been infected:
    (yx, d_yx, infected)
    """
    node = grid[tuple(yx)]
    grid[tuple(yx)] = (node + 1) % 4
    d_yx = turns[node] @ d_yx
    return yx + d_yx, d_yx, node == 1


infections = 0
yx = np.asarray([y+1, x+1]) // 2
d_yx = np.asarray([-1, 0])
for i_burst in range(10000000):
    yx, d_yx, infected = burst(yx, d_yx)
    infections += infected

print('Number of new infections: ', infections)
