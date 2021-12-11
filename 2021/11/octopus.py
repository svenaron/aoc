#!/usr/bin/env python

import numpy as np
from io import StringIO

sample = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def neighbours(a):
    a = np.pad(a, 1)
    return (np.roll(a,  1, [0, 1]) +
            np.roll(a, -1, [0, 1]) +
            np.roll(a, [1, -1], [0, 1]) +
            np.roll(a, [-1, 1], [0, 1]) +
            np.roll(a,  1, 0) +
            np.roll(a,  -1, 0) +
            np.roll(a,  1, 1) +
            np.roll(a,  -1, 1))[1:-1, 1:-1]


def flash(datafile, verify=False):
    octo = np.genfromtxt(datafile, delimiter=1, dtype=int)
    p1 = 0
    for i in range(10000):
        octo += 1
        flashed_this_step = np.zeros(np.shape(octo), dtype=int)
        while(np.any(octo > 9)):
            flashed_now = np.where(octo > 9, 1, 0)
            flashed_this_step |= flashed_now
            a = neighbours(flashed_now)
            a = np.where(flashed_this_step == 0, a, 0)
            octo += a
            octo[np.where(flashed_now)] = 0
        if i < 100:
            p1 += np.sum(flashed_this_step)
        if np.all(flashed_this_step):
            p2 = i+1
            break
    return p1, p2


def parse(f):
    return np.genfromtxt(f, delimiter=1, dtype=int)


if __name__ == "__main__":
    print("sample", flash(StringIO(sample), verify=True))
    with open('input') as f:
        print("input", flash(f))
