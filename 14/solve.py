import numpy as np


def knot_hash(value):
    lengths = list(map(ord, value)) + [17, 31, 73, 47, 23]

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
    return ''.join(map(lambda x: '{:02x}'.format(x), dense))


key_string = 'oundnydw'
hashes = map(lambda x: knot_hash('{}-{}'.format(key_string, x)), range(128))
bit_hashes = list(map(
    lambda h: ''.join(map(
        lambda hex_digit: '{:04b}'.format(int(hex_digit, 16)),
        h
    )),
    hashes
))
occupied = map(lambda x: x.count('1'), bit_hashes)
print('Number of used squares: ', sum(occupied))


# Part 2.
grid = np.asarray(list(map(lambda x: list(map(int, x)), bit_hashes)), dtype=int)


def update_grid(yx, d_yx, group_id):
    global grid

    # Do not use `+=` because this would modify `yx` in-place.
    yx = yx + d_yx
    if np.any((yx < 0) | (yx >= grid.shape)):  # Position outside of the grid.
        return
    if grid[tuple(yx)] == 0 or grid[tuple(yx)] == group_id:
        return
    assert grid[tuple(yx)] == 1, 'Encountered another group'
    grid[tuple(yx)] = group_id
    update_grid(yx, d_yx, group_id)
    update_grid(yx, np.roll(d_yx, 1), group_id)
    update_grid(yx, -np.roll(d_yx, 1), group_id)

while np.any(grid == 1):
    group_id = grid.max() + 1
    yx = np.argwhere(grid == 1)[0]
    grid[tuple(yx)] = group_id
    for d_yx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        update_grid(yx, np.asarray(d_yx), group_id)

print('Number of groups: ', grid.max()-1)
