def generator_a():
    val = 591
    while True:
        val = (val * 16807) % 2147483647
        yield val


def generator_b():
    val = 393
    while True:
        val = (val * 48271) % 2147483647
        yield val

ga = generator_a()
gb = generator_b()
matches = 0
for _ in range(40000000):
    a = next(ga) & 0xffff
    b = next(gb) & 0xffff
    matches += (a == b)

print('[Part 1] Number of matches: ', matches)


# Part 2.

def picky_generator_a():
    val = 591
    while True:
        val = (val * 16807) % 2147483647
        if val % 4 > 0:
            continue
        yield val


def picky_generator_b():
    val = 393
    while True:
        val = (val * 48271) % 2147483647
        if val % 8 > 0:
            continue
        yield val

ga = picky_generator_a()
gb = picky_generator_b()
matches = 0
for _ in range(5000000):
    a = next(ga) & 0xffff
    b = next(gb) & 0xffff
    matches += (a == b)

print('[Part 2] Number of matches: ', matches)
