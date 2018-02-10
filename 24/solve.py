with open('input.txt') as fp:
    components = [tuple([int(y) for y in x.rstrip().split('/')]) for x in fp]

starters = list(filter(lambda c: c[0] == 0 or c[1] == 0, components))
s_components = set(components)


def build(bridge, used, scores):
    """
    `bridge` contains the current number of pins the next component needs to be connected to.
    `used` is a set of all used components.
    `scores` contains the strength and number of components of all built bridges.
    """
    can_be_used = list(filter(
        lambda c: c[0] == bridge[-1] or c[1] == bridge[-1],
        s_components - set(used)
    ))
    if not can_be_used:
        scores.append((sum(map(sum, used)), len(used)))
        return
    for component in can_be_used:
        build(
            bridge + (component[1] if component[0] == bridge[-1] else component[0],),
            used | {component},
            scores
        )


scores = []
for starter in starters:
    build((max(starter),), {starter}, scores)

print('Strongest bridge: ', max(scores))
print('Longest bridge: ', max(scores, key=lambda x: tuple(reversed(x))))
