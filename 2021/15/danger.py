#!/usr/bin/env python

from cProfile import Profile
import numpy as np
from io import StringIO

sample = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


dirs = np.array(((1, 0), (0, 1), (-1, 0), (0, -1)))


def parse(data):
    return np.genfromtxt(StringIO(data), dtype=int, delimiter=1)


def ok(p, shape):
    return (p[0] >= 0 and p[0] < shape[0] and
            p[1] >= 0 and p[1] < shape[1])


def fill(cave, cache=None):
    if cache is None:
        cache = np.ones_like(cave) * 7000
        cache[0][0] = 0
    mx, my = cave.shape
    for dx, dy in zip(range(mx), range(my)):
        for y in range(dx):
            score((dx, y), cave, cache)
        for x in range(dy):
            score((x, dy), cave, cache)
        score((dx, dy), cave, cache)
    return cache


def score(p, cave, cache):
    pc = cave[p]
    for d in dirs:
        if not ok(p + d, cave.shape):
            continue
        ns = cache[tuple(p + d)]
        if ns + pc < cache[p]:
            cache[p] = ns + pc


def brute(cave):
    cache = fill(cave)
    s = [cache[-1][-1]]
    fill(cave, cache)
    s.append(cache[-1][-1])
    while s[-1] != s[-2]:
        fill(cave, cache)
        s.append(cache[-1][-1])
    return s[-1]


def expand(cave):
    c = cave.copy()
    for _ in range(4):
        c += 1
        c %= 10
        c = np.where(c == 0, 1, c)
        cave = np.concatenate((cave, c), 1)

    c = cave.copy()
    for _ in range(4):
        c += 1
        c %= 10
        c = np.where(c == 0, 1, c)
        cave = np.concatenate((cave, c))
    return cave


def walk(cave):
    p1 = brute(cave)
    bigcave = expand(cave)
    p2 = brute(bigcave)
    return (p1, p2)


if __name__ == "__main__":
    cave = parse(sample)
    s1, s2 = walk(cave)
    f1 = 40
    f2 = 315
    print("sample1", s1, f"INVALID (correct is {f1})" if s1 != f1 else "")
    print("sample2", s2, f"INVALID (correct is {f2})" if s2 != f2 else "")

    with open('input') as f:
        data = f.read().strip()
    cave = parse(data)
    print("input", walk(cave))
