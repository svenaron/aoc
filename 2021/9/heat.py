#!/usr/bin/env python

import numpy as np

sample = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def adjacent(i, length, cols):
    adj = [i-1 if i % cols > 0 else None,
           i+1 if i % cols < (cols - 1) else None,
           i+cols if i+cols < length else None,
           i-cols if i-cols >= 0 else None]
    return [a for a in adj if a is not None]


def spanbasin(i, data, length, cols, basin=None):
    if basin is None:
        basin = [i]
    new = [a for a in adjacent(i, length, cols)
           if data[a] != 9 and a not in basin]
    basin += new
    for c in new:
        spanbasin(c, data, length, cols, basin)
    return basin


def solve(data):
    cols = len(data.split("\n")[0])
    data = list(map(int, data.replace("\n", "")))
    length = len(data)

    low = [i for (i, d) in enumerate(data) if
           min(data[a] for a in adjacent(i, length, cols)) > d]
    p1 = sum(1+data[c] for c in low)

    basins = [spanbasin(c, data, length, cols) for c in low]
    bsum = sorted([len(b) for b in basins])
    p2 = np.prod(bsum[-3:])
    return p1, p2


if __name__ == "__main__":
    print("sample", solve(sample))
    with open('input') as f:
        data = f.read().strip()
    print("input", solve(data))
