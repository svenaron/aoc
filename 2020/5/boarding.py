#!/usr/bin/env python3
import sys

def parse(l):
    b = l.replace('F', '0').replace('B','1').replace('L', '0').replace('R','1')
    row = int(b[0:7], 2)
    col = int(b[7:10], 2)
    sid = row * 8 + col
    return (row, col, sid)


def getids(fname):
    with open(fname) as file:
        return [parse(l) for l in file if l.strip()]


if __name__ == "__main__":
    fname = sys.argv[1]
    sids = sorted([e[2] for e in getids(fname)])
    print(max(sids))
    gaps = [(a,b) for (a,b) in zip(sids, sids[1:]) if b != a+1]
    print(gaps)
