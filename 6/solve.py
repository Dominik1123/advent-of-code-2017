import numpy as np


with open('input.txt') as fp:
    counts = np.asarray(list(map(int, filter(None, fp.readline().split()))))

states = [counts.tolist()]

while True:
    bank = np.argmax(counts)
    count = counts[bank]
    counts[bank] = 0
    per_bank = count // counts.size
    remainder = count % counts.size
    counts += per_bank
    counts[(bank + 1 + np.arange(remainder)) % counts.size] += 1
    if counts.tolist() in states:
        break
    states.append(counts.tolist())

print('Number of operations: ', len(states))
print('Cycle length: ', len(states) - states.index(counts.tolist()))
