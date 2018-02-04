with open('input.txt') as fp:
    layers = list(map(lambda x: (int(x.split(':')[0]), int(x.split(':')[1])), fp))


def compute_position(pos, size, delay=0):
    # (size-1) steps are required for reaching from one end to the other.
    n_traversals = (pos+delay) // (size-1)
    remainder = (pos+delay) % (size-1)
    return remainder if n_traversals % 2 == 0 else (size-1) - remainder


def compute_severities(delay=0):
    global layers

    scanner_positions_at_arrival = map(
        lambda layer: compute_position(*layer, delay=delay),
        layers
    )

    return list(map(
        lambda x: (x[0] == 0)*x[1][0]*x[1][1],
        zip(scanner_positions_at_arrival, layers)
    ))

severities = compute_severities()

print('Severities: ', severities)
print('Trip severity: ', sum(severities))


# Part 2.

import itertools as it

for delay in it.count():
    if sum(compute_severities(delay)) == 0 and compute_position(*layers[0], delay=delay) > 0:
        print('Minimum required delay: ', delay)
        break
