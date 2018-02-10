from argparse import Namespace
import re


def parse_instruction(instr):
    match = re.match(r'^(?P<op>[a-z]+) (?P<op1>[a-z\d\-]+) ?(?P<op2>[a-z\d\-]+)?$', instr.strip())
    return match.groupdict()


with open('input.txt') as fp:
    instructions = list(map(parse_instruction, fp))

registers = dict(zip('abcdefgh', [0]*8))


def value(for_label):
    return int(registers.get(for_label, for_label))


def set_(op1, op2):
    def execute():
        registers[op1] = value(op2)
    execute.name = 'set'
    execute.operands = (op1, op2)
    return execute


def multiply(op1, op2):
    def execute():
        registers[op1] *= value(op2)
    execute.name = 'multiply'
    execute.operands = (op1, op2)
    return execute


def subtract(op1, op2):
    def execute():
        registers[op1] -= value(op2)
    execute.name = 'subtract'
    execute.operands = (op1, op2)
    return execute


def pass_(op1, op2):
    def execute():
        pass
    execute.name = 'pass'
    execute.operands = (op1, op2)
    return execute


def edge_to_next(next_node):
    def edge():
        return next_node
    edge.branches = (next_node,)
    return edge


def edge_jump_to(op1, branch_zero, branch_non_zero):
    def edge():
        return branch_zero if value(op1) == 0 else branch_non_zero
    edge.branches = (branch_zero, branch_non_zero)
    return edge


graph = {}
# Add operations.
for label, instruction in enumerate(instructions):
    op, op1, op2 = instruction['op'], instruction['op1'], instruction['op2']
    if op == 'set':
        operation = set_(op1, op2)
    elif op == 'mul':
        operation = multiply(op1, op2)
    elif op == 'sub':
        operation = subtract(op1, op2)
    elif op == 'jnz':
        operation = pass_(op1, op2)
    else:
        raise ValueError('Unknown operation: {}'.format(op))
    graph[label] = Namespace(label=label, operation=operation, edge=None)

# Add edges.
for label, node in graph.items():
    op = node.operation.name
    if op in ('set', 'multiply', 'subtract'):
        node.edge = edge_to_next(graph.get(label+1))
    elif op == 'pass':
        # Require that jump targets (offsets) are always constant
        # (i.e. not dependent on registers).
        op1, op2 = node.operation.operands
        node.edge = edge_jump_to(op1, graph.get(label+1), graph.get(label+value(op2)))
    else:
        raise ValueError('Unknown operation: {}'.format(op))

n_mul = 0
node = graph[0]
while node is not None:
    n_mul += (node.operation.name == 'multiply')
    node.operation()
    node = node.edge()

print('Number of "mul" instructions: ', n_mul)
