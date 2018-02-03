import numpy as np


with open('input.txt') as fp:
    digits = np.asarray(list(fp.read().strip()), dtype=int)

result = np.sum(digits[:-1][digits[:-1] == digits[1:]]) + digits[-1] * (digits[0] == digits[-1])
print('[Part 1] Result: ', result)


# Part 2.

digits2 = np.concatenate((digits, digits))
l2 = digits.size // 2
result2 = np.sum(digits[digits == digits2[l2:-l2]])
print('[Part 2] Result: ', result2)
