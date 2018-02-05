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


def collide(p):
    p_equal = np.equal.outer(p, p)
    p_equal = np.all(np.diagonal(p_equal, axis1=1, axis2=3), axis=2)
    np.fill_diagonal(p_equal, False)
    colliding = np.unique(np.argwhere(p_equal).flatten())
    return colliding


def check_expansion(p, v, a):
    """
    Check if each pair of particles increases their distance in at least one dimension and 
    has a tendency to do so in the future (i.e. acceleration is aligned with velocity
    for that dimension).
    """
    p2 = p + v + a
    expansion_value = np.abs(np.subtract.outer(p, p)) < np.abs(np.subtract.outer(p2, p2))
    expansion_value = np.diagonal(expansion_value, axis1=1, axis2=3)
    expansion_tendency = np.bitwise_and.outer(np.sign(v) == np.sign(a), np.sign(v) == np.sign(a))
    expansion_tendency = np.diagonal(expansion_tendency, axis1=1, axis2=3)
    expanding = np.any(expansion_value & expansion_tendency, axis=2)
    np.fill_diagonal(expanding, True)
    return np.all(expanding)


moving = np.ones(position.shape[0], dtype=bool)


def time_step():
    global position
    global velocity
    global acceleration
    global moving

    collided = collide(position[moving])
    is_moving = moving[moving]
    is_moving[collided] = False
    moving[moving] = is_moving[:]

    velocity[moving] += acceleration[moving]
    position[moving] += velocity[moving]


# Perform some time steps in order to decrease the number of particles that are still moving.
for step in range(256):
    time_step()

while not check_expansion(position[moving], velocity[moving], acceleration[moving]):
    time_step()
    step += 1

print('All collisions resolved after {} time steps. \n'
      'Still moving: {}.'.format(step+1, moving.sum()))
