""" This is a (simplified) translation of the puzzle input. """

a = d = e = f = g = h = 0
b = c = 81
# Part 2: Set a = 1.
# a = 1
# if a != 0:
#     b *= 100
#     b += 100000
#     c = b
#     c += 17000
# Part 2: b, c will have those values.
# b = 108100
# c = 125100
while True:
    f = 1
    d = 2
    while True:
        e = 2
        while True:
            if d * e == b:
                f = 0
            e += 1
            if e == b:
                break
        d += 1
        if d == b:
            break
    if f == 0:
        h += 1
    if b == c:
        break
    else:
        b += 17
