#!/usr/bin/env python

import re

rex = re.compile(
    r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')


def intersect(this, that):
    ranges = tuple(range(max(a.start, b.start), min(a.stop, b.stop))
                   for (a, b) in zip(this, that))
    return ranges if all(ranges) else None


def volume(cube):
    x, y, z = map(len, cube)
    return x*y*z


def unique_volume(cube, rest):
    overlap = [c for r in rest if (c := intersect(cube, r))]
    return volume(cube) - sum(unique_volume(c, overlap[i + 1:])
                              for i, c in enumerate(overlap))


def boot(cubes):
    done = []
    cnt = 0
    for on, c in reversed(cubes):
        if on:
            sz = unique_volume(c, done)
            if sz:
                cnt += sz
                done.insert(0, c)
        else:
            done.insert(0, c)
    return(cnt)


def parse(data, limit=None):
    cubes = []
    for mob in rex.finditer(data):
        points = tuple(map(int, mob.groups()[1:]))
        ranges = tuple(
            range(a, b + 1) for (a, b) in zip(points[::2], points[1::2]))
        if limit and not intersect(ranges, limit):
            continue
        cubes.append((mob.group(1) == 'on', ranges))
    return cubes


if __name__ == "__main__":
    with open('input') as f:
        data = f.read().strip()
    p1 = parse(data, (range(-50, 51),) * 3)
    p2 = parse(data)
    print("p1", boot(p1))
    print("p2", boot(p2))
