from collections import defaultdict
import re


def parse_instruction(instr):
    return re.match(r'^(?P<register>[a-z]+) '
                    r'(?P<op>dec|inc) '
                    r'(?P<value>-?[\d]+) '
                    r'if (?P<condition>(?P<depends_on>[a-z]+) (>|>=|==|!=|<=|<) -?[\d]+)$',
                    instr.strip()).groupdict()


with open('input.txt') as fp:
    instructions = list(map(parse_instruction, fp))

registers = defaultdict(int)
maximum = 0


def eval_instruction(instr):
    global registers
    global maximum

    if not eval(instr['condition'], {}, {instr['depends_on']: registers[instr['depends_on']]}):
        return

    op = {'inc': '+', 'dec': '-'}[instr['op']]
    registers[instr['register']] = eval(
        '{} {} {}'.format(instr['register'], op, instr['value']),
        {},
        {instr['register']: registers[instr['register']]}
    )
    maximum = max(maximum, registers[instr['register']])

for instruction in instructions:
    eval_instruction(instruction)

print('Register with largest value (currently): ', max(registers.items(), key=lambda x: x[1]))
print('Largest value ever: ', maximum)
