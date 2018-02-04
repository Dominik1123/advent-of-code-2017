import numpy as np
import string


with open('input.txt') as fp:
    diagram = np.asarray(list(map(
        lambda line: list(line.rstrip('\n')),
        fp
    )), dtype=str)

y = 0
x = np.argwhere(diagram[0] == '|').flatten()[0]
position = np.array([y, x])
velocity = np.array([0, 1], dtype=int)

characters = []
n_steps = 1

while True:
    current_site = diagram[tuple(position)]
    if current_site in string.ascii_uppercase:
        characters.append(current_site)

    if diagram[tuple(position + velocity)] == ' ':
        if diagram[tuple(position + np.roll(velocity, 1))] != ' ':
            velocity = np.roll(velocity, 1)
        elif diagram[tuple(position - np.roll(velocity, 1))] != ' ':
            velocity = -np.roll(velocity, 1)
        else:
            break

    position += velocity
    n_steps += 1

print('Characters encountered: ', ''.join(characters))
print('Number of steps: ', n_steps)
