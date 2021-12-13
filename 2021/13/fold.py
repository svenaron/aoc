#!/usr/bin/env python

import sys
import numpy as np
from io import StringIO

sample = ("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""", 17)


def parse(data):
    points, folds = data.split("\n\n")
    points = np.genfromtxt(StringIO(points), delimiter=',', dtype=int)
    folds = [f.split("=") for f in folds.split("\n")]
    folds = [(0, int(n)) if axis[-1] == 'x' else (1, int(n))
             for axis, n in folds]
    return points, folds


def fold(points, folds):
    for p in points:
        for i, n in folds:
            if p[i] > n:
                p[i] = n - (p[i] - n)


def points2str(points):
    mx = points[:, 0].max() + 1
    my = points[:, 1].max() + 1
    zeros = np.zeros((my, mx), dtype=int)
    for x, y in points:
        zeros[y][x] = 1
    return "\n".join("".join("█" if p else ' ' for p in line)
                     for line in zeros)


def origami(data):
    points, folds = parse(data)
    fold(points, folds[:1])
    p1 = len(set(tuple(p) for p in points))
    fold(points, folds[1:])
    return (p1, points2str(points))


if __name__ == "__main__":
    c, f1 = sample
    p1, p2 = origami(c.strip())
    print("sample", p1)
    print(p2)
    assert(p1 == f1)

    with open('input') as f:
        data = f.read().strip()
    p1, p2 = origami(data)
    print("input", p1)
    print(p2)
