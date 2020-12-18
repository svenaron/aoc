#!/usr/bin/env python3
import sys

move = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
    'F': [(1, 0), (0, 1), (-1, 0), (0, -1)],
}

def rotate(l, n):
    return l[n:] + l[:n]

def twist(x, y, d):
    return [(x, y), (y, -x), (-x, -y), (-y, x)][d % 4]

def manhattan(steps):
    (ew, ns) = (0, 0)
    for s, c in steps:
        if s in "LR":
            r = c // 90
            if s == 'R':
                r = -r
            move['F'] = rotate(move['F'], r)
        else:
            if s in 'F':
                dx = move[s][0][0] * c
                dy = move[s][0][1] * c
            else:
                dx = move[s][0] * c
                dy = move[s][1] * c
            ew += dx
            ns += dy
    return abs(ew) + abs(ns)

def waypoint(steps):
    (x, y) = (0, 0)
    (wx, wy) = (10, 1)
    for s, c in steps:
        if s in "LR":
            r = c // 90
            if s == 'L':
                r = -r
            wx, wy = twist(wx, wy, r)
        else:
            if s in 'F':
                x += wx * c
                y += wy * c
            else:
                wx += move[s][0] * c
                wy += move[s][1] * c
    print(x, y)
    return abs(x) + abs(y)

if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        steps = list(map(lambda x: (x[0], int(x[1:])),
                         f.read().strip().split("\n")))
    print(manhattan(steps))
    print(waypoint(steps))
