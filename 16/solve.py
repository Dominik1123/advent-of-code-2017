import re
import string

import numpy as np


def parse_move(move):
    match = re.match(r'([sxp])([\da-p]+)(/([\da-p]+))?', move)
    return match.groups()

with open('input.txt') as fp:
    moves = list(map(parse_move, fp.read().strip().split(',')))

abc = list(string.ascii_lowercase[:16])
programs = np.asarray(abc, dtype=str)


def dance(programs):
    for move, *details in moves:
        if move == 's':
            programs = np.roll(programs, int(details[0]))
        elif move == 'x':
            p1 = int(details[0])
            p2 = int(details[2])
            programs[p1], programs[p2] = programs[p2], programs[p1]
        elif move == 'p':
            p1 = np.argwhere(programs == details[0]).flatten()[0]
            p2 = np.argwhere(programs == details[2]).flatten()[0]
            programs[p1], programs[p2] = programs[p2], programs[p1]
    return programs

print('[Part 1] Programs: ', ''.join(dance(programs)))


# Part 2.
# Reset program positions to their initial state.
programs = np.asarray(abc, dtype=str)
n_dance = 1000000000
x_dance = 0
while x_dance < n_dance:
    x_dance += 1
    programs = dance(programs)
    if programs.tolist() == abc:
        print('Cycle detected (length {})'.format(x_dance))
        x_dance = n_dance - (n_dance % x_dance)

print('[Part 2] Programs: ', ''.join(programs))
