import numpy as np


step_size = 356
buffer = np.zeros(1, dtype=int)
position = 0

for val in range(1, 2018):
    position = (position + step_size) % val + 1
    buffer = np.insert(buffer, position, val)

print('Value after 2017: ', buffer[position+1])


# Part 2.

value_after_zero = None
for val in range(1, 50000000):
    position = (position + step_size) % val + 1
    if position == 1:
        value_after_zero = val

print('Value after 0: ', value_after_zero)
