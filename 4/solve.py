with open('input.txt') as fp:
    phrases = list(map(str.split, fp))

valid = filter(lambda x: len(x) == len(set(x)), phrases)
print('[Part 1] Number of valid passphrases: ', len(list(valid)))


# Part 2.

import itertools as it

valid2 = filter(
    lambda x: len(list(filter(
        lambda y: sorted(y[0]) == sorted(y[1]),
        it.combinations(x, 2)
    ))) == 0,
    phrases
)

print('[Part 2] Number of valid passphrases: ', len(list(valid2)))
