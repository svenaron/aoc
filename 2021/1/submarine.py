#!/usr/bin/env python

import numpy as np

sample = [199,
          200,
          208,
          210,
          200,
          207,
          240,
          269,
          260,
          263,]

def delta(indata):
    cnt = 0
    for a,b in zip(indata, indata[1:]):
        if b > a:
            cnt += 1

    print(cnt)

def sliding_window(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:]


if __name__ == "__main__":
    delta(sample)
    delta(sliding_window(sample, 3))
    with open('input') as f:
        data = list(map(int, f.readlines()))
    delta(data)
    delta(sliding_window(data, 3))
