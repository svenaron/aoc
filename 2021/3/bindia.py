#!/usr/bin/env python

import numpy as np

sample = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split("\n")

def toint(lst):
    return [int(x) for x in lst]

def bindia(data):
    res = np.array(list(map(toint, map(list, data))))
    g = int("".join(['1' if x >= 0.5 else '0'
                             for x in np.average(res, 0)]), 2)
    e = ~g & int("1" * len(data[0].strip()), 2)
    print(g, e, g*e)

def findrating(data, bitpos, func):
    rate = np.average(data, 0)
    bv = func(rate[bitpos])
    data = [d for d in data if d[bitpos] == bv]
    if (len(data) == 1):
        return int("".join(map(str, data[0])), 2)
    return findrating(data, bitpos + 1, func)

def oxyrating(data):
    def func(v):
        return 1 if v >= 0.5 else 0
    return findrating(data, 0, func)

def co2rating(data):
    def func(v):
        return 1 if v < 0.5 else 0
    return findrating(data, 0, func)

def part2(rawdata):
    data = np.array(list(map(toint, map(list, rawdata))))
    a = oxyrating(data)
    b = co2rating(data)
    print(a, b, a*b)

if __name__ == "__main__":
    bindia(sample)
    part2(sample)
    with open('input') as f:
        data = f.read().strip().split('\n')
    bindia(data)
    part2(data)
