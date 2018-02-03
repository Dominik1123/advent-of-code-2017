with open('input.txt') as fp:
    instructions = list(map(int, fp))

steps = 0
pointer = 0
while 0 <= pointer + instructions[pointer] < len(instructions):
    instructions[pointer] += 1
    pointer += (instructions[pointer] - 1)
    steps += 1

print('[Part 1] Number of steps: ', steps+1)


# Part 2.

with open('input.txt') as fp:
    instructions = list(map(int, fp))

steps = 0
pointer = 0
while 0 <= pointer + instructions[pointer] < len(instructions):
    old_pointer = pointer
    pointer += instructions[pointer]
    instructions[old_pointer] += 1 if instructions[old_pointer] < 3 else -1
    steps += 1

print('[Part 2] Number of steps: ', steps + 1)
