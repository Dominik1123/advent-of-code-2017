import numpy as np


with open('input.txt') as fp:
    lengths = list(map(int, fp.readline().split(',')))

numbers = np.arange(256)
index = 0
skip = 0
for l in lengths:
    selection = (np.arange(l) + index) % 256
    numbers[selection] = np.flip(numbers[selection], 0)
    index = (index + l + skip) % 256
    skip += 1

print('Product: ', numbers[0] * numbers[1])


# Part 2.

with open('input.txt') as fp:
    lengths = list(map(ord, fp.readline().strip())) + [17, 31, 73, 47, 23]

numbers = np.arange(256)
index = 0
skip = 0
for _ in range(64):
    for l in lengths:
        selection = (np.arange(l) + index) % 256
        numbers[selection] = np.flip(numbers[selection], 0)
        index = (index + l + skip) % 256
        skip += 1

dense = np.bitwise_xor.reduce(numbers.reshape((16, 16)), axis=1)
print('Hash value: ', ''.join(map(lambda x: '{:02x}'.format(x), dense)))
