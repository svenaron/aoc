#!/usr/bin/env python

import numpy as np

sample = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def toint(foo):
    try:
        return int(foo)
    except:
        return [toint(f) for f in foo]

def rng(a, b):
    if a > b:
        return range(a, b - 1, -1)
    return range(a, b + 1, 1)

def draw(line):
    (x1, y1), (x2, y2) = line
    x = rng(x1, x2)
    y = rng(y1, y2)
    if len(x) == 1:
        x = [x1] * len(y)
    if len(y) == 1:
        y = [y1] * len(x)
    return zip(x, y)

def vents(data, simple=True):
    lines = [x.replace(" -> ", ",").split(",") for x in data.split("\n")]
    lines = toint([(x[0:2], x[2:]) for x in lines])
    if simple:
        lines = [l for l in lines if l[0][0] == l[1][0] or l[0][1] == l[1][1]]
    lines = [set(draw(l)) for l in lines]
    intersections = dict()
    for a in lines:
        for b in lines:
            if a == b:
                continue
            for i in a.intersection(b):
                intersections.setdefault(i, []).append(i)

    return len([x for x in intersections.items() if len(x) > 1])

if __name__ == "__main__":
    print(vents(sample))
    with open('input') as f:
        data = f.read().strip()
    print(vents(data), vents(data, False))
