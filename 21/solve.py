import numpy as np


def parse_pattern(pattern):
    in_, out = map(str.strip, pattern.split('=>'))
    in_ = list(map(list, in_.split('/')))
    out = list(map(list, out.split('/')))
    return np.asarray(in_, dtype=str), np.asarray(out, dtype=str)


with open('input.txt') as fp:
    _patterns = list(map(parse_pattern, fp))

patterns = {
    2: list(filter(lambda p: p[0].shape == (2, 2), _patterns)),
    3: list(filter(lambda p: p[0].shape == (3, 3), _patterns)),
}


def match_pattern(square):
    for flipped in (square, np.flip(square, axis=0)):
        for rotate in range(4):
            transformed = np.rot90(flipped, k=rotate)
            try:
                pattern = next(filter(
                    lambda p: np.array_equal(p[0], transformed),
                    patterns[square.shape[0]]
                ))
            except StopIteration:
                continue
            else:
                return pattern[1]
    raise ValueError('Square does not match any pattern:\n{}'.format(square))

initial_image = np.asarray([
    list('.#.'),
    list('..#'),
    list('###')
])

size = 3
for _ in range(18):
    if size % 2 == 0:
        size += (size // 2)
    elif size % 3 == 0:
        size += (size // 3)

print('Resulting image size: {} x {}'.format(size, size))

image = np.full([size]*2, 'x', dtype=str)
image[:3, :3] = initial_image.copy()

size = square_size = 3
for i in range(18):
    if size % 2 == 0:
        square_size = 2
        n_squares = size // 2
        size += (size // 2)
    elif size % 3 == 0:
        square_size = 3
        n_squares = size // 3
        size += (size // 3)
    else:
        raise ValueError('size is neither divisible by 2 nor 3')

    for j in reversed(range(n_squares)):
        for k in reversed(range(n_squares)):
            # Replace old square at coordinates (y0, x0) with new square at coordinates (y1, x1).
            x0 = j * square_size
            y0 = k * square_size
            x1 = j * (square_size + 1)
            y1 = k * (square_size + 1)
            image[y1 : y1 + (square_size + 1), x1 : x1 + (square_size + 1)] = match_pattern(
                image[y0: y0 + square_size, x0: x0 + square_size]
            )

    if i == 4:
        print(image)
        print('Elements on after 5 iterations: ', np.count_nonzero(image == '#'))

print(image)
print('Elements on after 18 iterations: ', np.count_nonzero(image == '#'))
