#!/usr/bin/env python3
import sys
import itertools

init = """
##......
.##...#.
.#######
..###.##
.#.###..
..#.####
##.####.
##..#.##
""".strip()

sample = """
.#.
..#
###
""".strip()

def load(data, dims = 3):
    return {(x, y) + (0,) * (dims - 2)
            for (y, line) in enumerate(data.split('\n'))
            for (x, s) in enumerate(line.strip()) if s == '#'}

def neighbors(point):
    return set(itertools.product(
        *(range(p - 1, p + 2) for p in point))) - {point}

def cycle(active):
    inactive = {n for p in state for n in neighbors(p) if n not in state}
    on = {p for p in inactive
          if len(neighbors(p).intersection(state)) == 3}
    off = {p for p in state
           if len(neighbors(p).intersection(state)) not in [2,3]}
    active.difference_update(off)
    active.update(on)

def pretty_print(state):
    zs = [p[2] for p in state]
    ys = [p[1] for p in state]
    xs = [p[0] for p in state]
    for z in range(min(zs), 1 + max(zs)):
        print("z =", z)
        for y in range(min(ys), 1 + max(ys)):
            print("".join(['#' if (x, y, z) in state else "."
                           for x in range(min(xs), 1 + max(xs))]))
        print("")

if __name__ == "__main__":
    # sample data
    state = load(sample)
    for _ in range(6):
        cycle(state)
    print(len(state))

    # part 1
    state = load(init, 3)
    for _ in range(6):
        cycle(state)
    print(len(state))

    # part 2
    state = load(init, 4)
    for _ in range(6):
        cycle(state)
    print(len(state))
