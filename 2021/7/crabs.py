#!/usr/bin/env python

import numpy as np

sample = "16,1,2,0,4,2,7,1,2,14"

def c3(nums, p, price):
    r = {cost(nums, p - 1, price): -1,
         cost(nums, p, price): 0,
         cost(nums, p + 1, price): 1}
    return min(r), r[min(r)]

def crabs(data):
    nums = np.array(list(map(int, data.split(','))))
    p1 = int(sum(abs(nums - np.median(nums))))

    price = {i:sum(range(i+1)) for i in range(min(nums), max(nums))}
    m = np.median(nums)
    p2, d = c3(nums, m, price)
    while d != 0:
        m += d
        p2, d = c3(nums, m, price)
    return p1, p2

def cost(nums, pos, price):
    r = [price[x] for x in abs(nums - pos)]
    return sum(r)

if __name__ == "__main__":
    print("sample", crabs(sample))
    with open('input') as f:
        data = f.read().strip()
    print("input", crabs(data))
