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
    except TypeError:
        op2_value = None
    if operation == 'snd':
        return 1, op1_value
    elif operation == 'set':
        registers[operand1] = op2_value
    elif operation == 'add':
        registers[operand1] += op2_value
    elif operation == 'mul':
        registers[operand1] *= op2_value
    elif operation == 'mod':
        registers[operand1] %= op2_value
    elif operation == 'rcv' and op1_value != 0:
        return 1, 'recovered'
    elif operation == 'jgz' and op1_value > 0:
        return op2_value, None
    return 1, None


index = 0
frequency = None
most_recently_played = None
while 0 <= index < len(instructions):
    (increment, frequency), most_recently_played = \
        follow(instructions[index]), frequency or most_recently_played
    index += increment
    if frequency == 'recovered':
        print('Most recently played sound: ', most_recently_played)
        break
