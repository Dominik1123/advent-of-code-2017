"""
    Numbers contained in the i-th square: `(i > 0): 4 * (2i + 1) - 4 = 8i`.
    Having n squares requires therefore `1 + 4*n*(n+1)` numbers.
    The given memory location makes up n squares + some rest:
        
        location = 1 + 4n(n+1) + rest
        
    The edge length of the i-th square is given by: `2i + 1`.
    
    Having completed exactly n squares yields position (n, n).
    Having completed an additional m (edges-1) of the n+1 square yields position:
    
        * m = 1: (n+1, -(n+1))
        * m = 2: (-(n+1), -(n+1))
        * m = 3: (-(n+1), n+1)
        
    Having completed an additional l steps yields positions:
    
        * m = 0: (n+1, n-l)
        * m = 1: (n+1-l, -(n+1))
        * m = 2: (-(n+1), -(n+1)+l)
        * m = 3: (-(n+1)+l, n+1)
        
    So we can decompose the location in the number of squares completed + the number of edges
    completed + the remaining steps and compute its (x, y) from the above relations.
    The Manhattan distance is given by sum(abs(x, y)).
    
    Actually we can shortcut the above procedure and not differentiate between the different
    number-of-edges cases as for the Manhattan distance it doesn't matter in which quadrant
    the memory is located. Therefore we can simply compute the number of steps as the remainder
    dividing the squares-remainder by the (edge-1) length.
"""

location = 265149

sum_squares = lambda x: 1 + 4*x*(x + 1)
n_squares = 1
while sum_squares(n_squares) < location:
    n_squares += 1
n_squares -= 1

remainder = location - sum_squares(n_squares)
n_edges = remainder // (2*(n_squares+1))
n_steps = remainder % (2*(n_squares+1))

x_y_location = {
    0: lambda n, l: (n+1, n-l),
    1: lambda n, l: (n+1-l, -(n+1)),
    2: lambda n, l: (-(n+1), -(n+1)+l),
    3: lambda n, l: (-(n+1)+l, n+1),
}[n_edges](n_squares, n_steps)

print('n_squares: ', n_squares)
print('n_edges: ', n_edges)
print('n_steps: ', n_steps)
print('(x, y): ', x_y_location)
print('Manhattan distance: ', sum(map(abs, x_y_location)))

# Shortcut.
print('\n=== Shortcut ===')
if remainder == 0:
    distance = 2*n_squares
else:
    n_steps = remainder % (2*(n_squares+1))
    distance = (n_squares+1) + abs(n_squares+1 - n_steps)
    print('n_steps: ', n_steps)
print('Manhattan distance: ', distance)


# Part 2.

import numpy as np

# Number of squares requires to cover the input number (not the sum). As the sum within each site
# is greater or equal than its number, it's sufficient to allocate space equal to the number.
n_squares_required = int(np.sqrt(1 + location/2) - 0.5)
edge_length = 2*n_squares_required + 1
memory = np.zeros(shape=(edge_length, edge_length), dtype=int)

x = y = edge_length // 2
memory[y, x] = 1
x += 1

# ns: the number of the square that is currently processed.
# visited: the number of sites already visited.
ns = 1
visited = 1
while True:
    memory[y, x] += (
        memory[y-1, x-1] + memory[y-1, x] + memory[y-1, x+1]
        + memory[y, x-1] + memory[y, x+1]
        + memory[y+1, x-1] + memory[y+1, x] + memory[y+1, x+1]
    )
    if memory[y, x] > location:
        print('Result: ', memory[y, x])
        break
    visited += 1
    if visited < 30:
        print('#{}: {}'.format(visited, memory[y, x]))
    if (visited - 1 - 4*ns*(ns+1)) == 0:  # Square complete.
        ns += 1
        x += 1
        continue
    which_edge = (visited - 1 - 4*ns*(ns-1)) // (2*ns)
    if which_edge == 0:
        y -= 1
    elif which_edge == 1:
        x -= 1
    elif which_edge == 2:
        y += 1
    else:
        x += 1
