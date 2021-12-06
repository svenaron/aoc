#!/usr/bin/env python

import numpy as np

sample = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split("\n")

dirs = {'d':(1, 0), 'u':(-1, 0), 'f':(0, 1)}

def pilot1(data):
    steps = [np.array(dirs[x[0]])* int(x.split()[-1]) for x in data]
    result = np.sum(steps, 0)
    print(result, np.prod(result))

def pilot2(data):
    steps = [np.array(dirs[x[0]])* int(x.split()[-1]) for x in data]
    aim = 0
    result = [0, 0]
    for s in steps:
        if s[0] == 0:
            result[0] += aim * s[1]
            result[1] += s[1]
        else:
            aim += s[0]
    print(result, np.prod(result))


if __name__ == "__main__":
    pilot1(sample)
    pilot2(sample)
    with open('input') as f:
        data = f.readlines()
    pilot1(data)
    pilot2(data)
