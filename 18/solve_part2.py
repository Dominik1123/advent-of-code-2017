from collections import defaultdict
from queue import Queue
import re
import threading
import time


class Program(threading.Thread):
    def __init__(self, nr, in_queue, out_queue, instructions, supervisor):
        super().__init__()
        self.nr = nr
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._instructions = instructions
        self._supervisor = supervisor
        self._registers = defaultdict(int)
        self._registers['p'] = nr
        self._n_out = 0

    def follow(self, instruction):
        operation = instruction['op']
        operand1, operand2 = instruction['op1'], instruction['op2']
        try:
            op1_value = int(operand1)
        except ValueError:
            op1_value = self._registers[operand1]
        try:
            op2_value = int(operand2)
        except ValueError:
            op2_value = self._registers[operand2]
        except TypeError:
            op2_value = None
        if operation == 'snd':
            self._out_queue.put(op1_value)
            self._n_out += 1
        elif operation == 'set':
            self._registers[operand1] = op2_value
        elif operation == 'add':
            self._registers[operand1] += op2_value
        elif operation == 'mul':
            self._registers[operand1] *= op2_value
        elif operation == 'mod':
            self._registers[operand1] %= op2_value
        elif operation == 'rcv':
            if self._in_queue.empty():
                self._supervisor.notify_wait[self.nr].set()
            val = self._in_queue.get(block=True)
            self._supervisor.notify_wait[self.nr].clear()
            if val == 'stop':
                return None
            self._registers[operand1] = val
        elif operation == 'jgz' and op1_value > 0:
            return op2_value
        return 1

    def run(self):
        index = 0
        while 0 <= index < len(self._instructions):
            try:
                index += self.follow(self._instructions[index])
            except TypeError:
                print('[Program {}] Stopped by supervisor'.format(self.nr))
                break
        else:
            print('[Program {}] Terminated regularly'.format(self.nr))
        self._supervisor.has_terminated[self.nr].set()


class Supervisor(threading.Thread):
    def __init__(self, msg_queues):
        super().__init__()
        self.notify_wait = [threading.Event(), threading.Event()]
        self.has_terminated = [threading.Event(), threading.Event()]
        self._msg_queues = msg_queues

    def run(self):
        while True:
            if self.notify_wait[0].is_set() and self.notify_wait[1].is_set() \
                    and self._msg_queues[0].empty() and self._msg_queues[1].empty():
                for q in self._msg_queues:
                    q.put('stop')
                break
            if self.has_terminated[0].is_set() and self.has_terminated[1].is_set():
                break
            time.sleep(0.1)


def parse_instruction(instr):
    match = re.match(r'^(?P<op>[a-z]+) (?P<op1>[a-z\d\-]+) ?(?P<op2>[a-z\d\-]+)?$', instr.strip())
    return match.groupdict()


with open('input.txt') as fp:
    instructions = list(map(parse_instruction, fp))

msg_queue_0 = Queue()
msg_queue_1 = Queue()
supervisor = Supervisor((msg_queue_0, msg_queue_1))
program_0 = Program(0, msg_queue_0, msg_queue_1, instructions, supervisor)
program_1 = Program(1, msg_queue_1, msg_queue_0, instructions, supervisor)

supervisor.start()
program_0.start()
program_1.start()
supervisor.join()
program_0.join()
program_1.join()

print('Number of transmissions: ', program_1._n_out)
