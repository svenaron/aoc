#!/usr/bin/env python

import re

target = {'A': ((4, 2), (3, 2), (2, 2), (1, 2)),
          'B': ((4, 4), (3, 4), (2, 4), (1, 4)),
          'C': ((4, 6), (3, 6), (2, 6), (1, 6)),
          'D': ((4, 8), (3, 8), (2, 8), (1, 8))}
cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def print_cave(cave, best):
    cl = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
          ['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#'],
          [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
          [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
          [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#'],
          [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
    for (x, y), p in cave.items():
        if p:
            cl[x+1][y+1] = p
    print(best)
    print("\n".join("".join(line) for line in cl))
    print("")


def manhattan(a, b, p):
    d = sum(abs(val1 - val2) for val1, val2 in zip(a, b))
    return d * cost[p]


def parse(data):
    cave = {(1 + i // 4, i % 4 * 2 + 2): p
            for (i, p) in enumerate(re.findall('([ABCD])', data))}
    return cave


def possible(cave):
    res = 0
    for c, p in cave.items():
        if c in target[p]:
            continue
        res += manhattan(c, (0, target[p][1][1]), p) + cost[p]
    return res


def exits(cave, c, p):
    done = []
    for d in target[p]:
        if cave.get(d) != p:
            break
        done.append(d)
    if c in done:
        return []  # done, no need to move
    if c[0] > 1 and any((r, c[1]) in cave for r in range(c[0] - 1, 0, -1)):
        return []  # can't move
    if c[0]:
        # from room to hallway
        exits = []
        for opts in (range(c[1] - 1, -1, -1), range(c[1] + 1, 11)):
            for h in opts:
                if h in (2, 4, 6, 8):
                    continue
                if (0, h) in cave:
                    break
                exits.append((0, h))
        return exits
    else:
        # from hallway to room
        if any(cave.get(c) not in (None, p) for c in target[p]):
            return []  # can't move
        tgt = target[p][0][1]  # target hallway room
        d = -1 if c[1] > tgt else 1
        steps = range(c[1] + d, tgt + d, d)
        if any((0, h) in cave for h in steps):
            return []  # can't move
        for c in target[p]:
            if c not in cave:
                return [c]  # move to innermost free room


def move(cave, score=0, best=None, moves=None, tried=None):
    if moves is None:
        moves = tuple()
    if best is None:
        best = [50000]
    if tried is None:
        tried = set()
    if moves in tried:
        return best[0]
    if score + possible(cave) > best[0]:
        return best[0]
    if all(c in target[p] for c, p in cave.items() if p):
        return score
    for c, p in sorted(cave.items()):
        for e in exits(cave, c, p):
            if score + manhattan(c, e, p) > best[0]:
                continue
            nc = cave.copy()
            nc[e] = nc.pop(c)
            nm = tuple(sorted(moves + ((p, c, e),)))
            ns = move(nc, score + manhattan(c, e, p), best, nm, tried)
            if ns < best[0]:
                print("best", ns)
                best[0] = ns
    tried.add(moves)
    return best[0]


if __name__ == "__main__":
    with open('input2') as f:
        data = f.read().strip()
    cave = parse(data)
    print(move(cave))
