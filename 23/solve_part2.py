# See `program.py` for details of the program structure.
# b = 108100
# c = 125100
# The outermost while loop runs until b == c whereat b is increased by 17 at the end of each
# iteration. Because `c = b + 17000` there will be a total of 1001 iterations.
# Let `i` be the iteration index. If `108100 + i*17` is not prime then f will be set to zero which
# will cause h to be increased by 1 subsequently.
# Therefore h contains the number of times `108100 + i*17` is not prime.


def is_prime(n):
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def is_not_prime(x):
    return not is_prime(x)

print(
    'Value in register h: ',
    sum(map(is_not_prime, map(lambda i: 108100 + i*17, range(1001))))
)
