from collections import defaultdict
import re


tape = defaultdict(int)


def write_value(value):
    def write(index, state):
        global tape
        tape[index] = value
        return index, state
    return write


def move_pointer(offset):
    def move(index, state):
        return index + offset, state
    return move


def change_state(new_state):
    def change(index, state):
        return index, new_state
    return change


with open('input.txt') as fp:
    m = re.match(r'^Begin in state ([A-Z])\.$', fp.readline().rstrip())
    start_state = m.groups()[0]
    m = re.match(r'^Perform a diagnostic checksum after (\d+) steps.$', fp.readline().rstrip())
    n_steps = int(m.groups()[0])
    fp.readline()

    blueprint = defaultdict(list)

    def _read_block():
        m = re.match(r'^In state ([A-Z]):$', fp.readline().rstrip())
        if m is None:
            return False
        current_state = m.groups()[0]

        for value in (0, 1):
            fp.readline()

            m = re.match(r'^Write the value ([01])\.$', fp.readline().strip()[2:])
            blueprint[(current_state, value)].append(
                write_value(int(m.groups()[0])))

            m = re.match(r'^Move one slot to the (left|right)\.$', fp.readline().strip()[2:])
            blueprint[(current_state, value)].append(
                move_pointer(-1 if m.groups()[0] == 'left' else 1))

            m = re.match(r'^Continue with state ([A-Z])\.$', fp.readline().strip()[2:])
            blueprint[(current_state, value)].append(
                change_state(m.groups()[0]))

        fp.readline()

        return True

    while _read_block():
        pass


index = 0
state = start_state
for _ in range(n_steps):
    for action in blueprint[(state, tape[index])]:
        index, state = action(index, state)

print('Checksum: ', sum(tape.values()))
