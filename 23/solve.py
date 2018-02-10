from collections import defaultdict
import re


def parse_instruction(instr):
    match = re.match(r'^(?P<op>[a-z]+) (?P<op1>[a-z\d\-]+) ?(?P<op2>[a-z\d\-]+)?$', instr.strip())
    return match.groupdict()


with open('input.txt') as fp:
    instructions = list(map(parse_instruction, fp))

registers = defaultdict(int)


def follow(instruction):
    global registers

    operation = instruction['op']
    operand1, operand2 = instruction['op1'], instruction['op2']
    try:
        op1_value = int(operand1)
    except ValueError:
        op1_value = registers[operand1]
    try:
        op2_value = int(operand2)
    except ValueError:
        op2_value = registers[operand2]
    if operation == 'set':
        registers[operand1] = op2_value
    elif operation == 'sub':
        registers[operand1] -= op2_value
    elif operation == 'mul':
        registers[operand1] *= op2_value
    elif operation == 'jnz' and op1_value != 0:
        return op2_value
    return 1


n_mul = 0
index = 0
while 0 <= index < len(instructions):
    n_mul += (instructions[index]['op'] == 'mul')
    index += follow(instructions[index])

print('Number of "mul" instructions: ', n_mul)
