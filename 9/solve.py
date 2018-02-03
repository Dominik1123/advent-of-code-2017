with open('input.txt') as fp:
    stream = fp.read().strip()

group_scores = []
garbage_count = 0


def dive_group(start_index, level):
    global group_scores
    global garbage_count

    group_scores.append(level)
    garbage = False
    index = start_index
    while True:
        index += 1
        char = stream[index]
        if char == '}' and not garbage:
            return index
        elif char == '{' and not garbage:
            index = dive_group(index, level+1)
        elif char == '<':
            garbage_count += garbage
            garbage = True
        elif char == '>':
            garbage = False
        elif char == '!':
            index += 1
        elif garbage:
            garbage_count += 1

assert dive_group(0, 1) == len(stream)-1, 'Did not parse the whole stream'
print('Group score: ', sum(group_scores))
print('Garbage count: ', garbage_count)
