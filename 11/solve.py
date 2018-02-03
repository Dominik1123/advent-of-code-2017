import json
import numpy as np


with open('input.txt') as fp:
    path = fp.readline().strip()

# Directions are nw-se (index 0), n-s (index 1) and sw-ne (index 2).
vectors = np.asarray(json.loads(
    '[' + path.replace('nw', '[1,0,0]').replace('se', '[-1,0,0]')
              .replace('ne', '[0,0,1]').replace('sw', '[0,0,-1]')
              .replace('n', '[0,1,0]').replace('s', '[0,-1,0]') + ']',
    ),
    dtype=int
)
distance = vectors.sum(axis=0)


def as_xy_coordinates(dist):
    x, y = -dist[0], dist[1]
    x += dist[2]
    y += dist[2]
    return x, y


def distance_from_xy(x, y):
    return abs(x - y) + min(x, y)


print('Number of steps: ', distance_from_xy(*as_xy_coordinates(distance)))


# Part 2.

distances = np.cumsum(vectors, axis=0)
steps = np.apply_along_axis(lambda d: distance_from_xy(*as_xy_coordinates(d)), 1, distances)
print('Maximum number of steps ever: ', steps.max())
