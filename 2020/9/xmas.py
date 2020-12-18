#!/usr/bin/env python3
import sys

def getnums(fname):
    with open(fname) as file:
        return list(map(int, file.read().strip().split('\n')))

def check1(data):
    nums = data[:-1]
    return [(a, b) for a in nums
            for b in nums if a + b == data[-1]]

def step1(numbers, n):
    idx = n
    while check1(numbers[idx - n:idx + 1]):
        idx += 1
    return numbers[idx]

def step2(numbers, s1):
    for l in range(2, len(numbers)):
        for i in range(0, len(numbers)):
            if sum(numbers[i:i+l]) == s1:
                a = min(numbers[i:i+l])
                b = max(numbers[i:i+l])
                return a+b

if __name__ == "__main__":
    fname = sys.argv[1]
    cnt = int(sys.argv[2])
    nums = getnums(fname)
    s1 = step1(nums, cnt)
    s2 = step2(nums, s1)
    print(s1)
    print(s2)
