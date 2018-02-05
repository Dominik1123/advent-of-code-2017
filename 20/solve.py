import re

import numpy as np


def parse_particle(description):
    match = re.match(r'^p=<([\d,\-]+)>, v=<([\d,\-]+)>, a=<([\d,\-]+)>$', description.strip())
    return list(map(lambda x: x.split(','), match.groups()))

with open('input.txt') as fp:
    position, velocity, acceleration = zip(*map(parse_particle, fp))

position = np.asarray(position, dtype=int)
velocity = np.asarray(velocity, dtype=int)
acceleration = np.asarray(acceleration, dtype=int)

# From recursion we deduce
#
#     p_i+1   =   p_i   +   v_i   +   a
#             =   p_i-1 + 2*v_i-1 + 3*a
#           [...]
#             =   p_0 + (i+1)*v_0 + (i+1)*(i+2)/2*a
#
# This is dominated by the acceleration term and so we use it to determine the closest particle.

print('Closest particle: ', np.argmin(np.abs(acceleration).sum(axis=1)))
