#!/usr/bin/env python2
import sys

def nextdep(ts, bus):
    assert(ts > 0)
    y = (bus - (ts % bus)) % bus
    return y

def nextbus(ts, lines):
    return [(nextdep(ts, x), x) for x in [int(x) for x in lines if x != 'x']]

def check2(lines, ts):
    r = 1
    for (i, b) in lines:
        if (ts + i) % b == 0:
            r *= b
        else:
            return r
    return 0

def nextt2(lines, dontcare = 0):
    lines = [(i, int(t)) for (i, t) in enumerate(lines) if t != 'x']
    ts = lines[0][1]
    d = ts
    i = 0
    while d > 0:
        ts += d
        d = check2(lines, ts)
        i += 1
    return ts

if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        ts = int(f.readline())
        lines = f.read().strip().split(',')
    nxt = sorted(nextbus(ts, lines))
    print(nxt)
    print(nxt[0][0] * nxt[0][1])

    ts = int(sys.argv[2] if len(sys.argv) > 2 else 0)
    print(nextt2(lines, ts))
