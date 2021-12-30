#!/usr/bin/env python

import numpy as np
from io import StringIO
import re


def parse(data):
    east = StringIO(re.sub('>', 'True ', re.sub('[v.]', 'False ', data)))
    east = np.genfromtxt(east, dtype=bool)
    south = StringIO(re.sub('v', 'True ', re.sub('[>.]', 'False ', data)))
    south = np.genfromtxt(south, dtype=bool)
    return (east, south)


def move(cuc, occ, d):
    moved = np.roll(cuc, 1, d)
    good = moved & ~occ
    bad = moved & occ
    return (np.roll(bad, -1, d) | good, np.sum(good))


def step(east, south):
    east, ec = move(east, east | south, 1)
    south, sc = move(south, east | south, 0)
    return ((east, south), ec + sc)


if __name__ == "__main__":
    with open('input') as f:
        data = parse(f.read().strip())
    data, cnt = step(*data)
    s = 1
    while cnt:
        data, cnt = step(*data)
        s += 1
    print("p1", s, "steps")
