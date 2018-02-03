import itertools as it
import re
import numpy as np


with open('input.txt') as fp:
    rows = np.asarray(list(map(lambda x: re.sub(r'[\s\t]+', ',', x.strip()).split(','), fp)),
                      dtype=int)

result = np.sum(rows.max(axis=1) - rows.min(axis=1))
print('[Part 1] Result: ', result)


# Part 2.

quotients = map(
    lambda x: max(x) // min(x),
    map(
        lambda y: next(filter(
            lambda z: max(z) % min(z) == 0,
            it.combinations(y, 2)
        )),
        rows
    )
)
result2 = sum(quotients)
print('[Part 2] Result: ', result2)
