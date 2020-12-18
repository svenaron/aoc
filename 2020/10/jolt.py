#!/usr/bin/env python3
import sys

def gaps(data):
    numbers = [0] + sorted(data)
    numbers.append(numbers[-1] + 3)
    count = [0, 0, 0]
    for (a, b) in zip(numbers, numbers[1:]):
        idx = b - a - 1
        if idx < 0 or idx > 2:
            raise Exception("bad data?")
        count[idx] = count[idx] + 1
    return count

def cheatcount(data):
    c = 1
    streak = 0
    for i in range(len(data) - 1):
        if data[i] == data[i+1] - 1:
            streak += 1
        else:
            c *= combo(streak)
            print(f"streak of {streak} broken at index {i}, count is {c}")
            streak = 0
    return c

cache = {}
def combo(l, c = 0, quick = True):
    if c > l:
        return 0
    if c == l:
        return 1
    if l - c in cache:
        return cache[l - c]
    r = sum([combo(l, c + x) for x in [1, 2, 3]])
    if quick:
        cache[l - c] = r
    return r

if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        numbers = sorted(map(int, f.read().strip().split('\n')))
    c = gaps(numbers)
    print(c[0] * c[2], c)
    print(cheatcount([0] + numbers + [max(numbers)]))
