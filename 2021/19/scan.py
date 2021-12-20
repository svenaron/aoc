#!/usr/bin/env python

import numpy as np
from io import StringIO
from itertools import permutations


def perms(arr):
    for columns in permutations(range(3)):
        for x in (1, -1):
            for y in (1, -1):
                for z in (1, -1):
                    a = arr[:, columns] * [x, y, z]
                    a = a[np.lexsort(np.rot90(a))]
                    for r in range(len(a)):
                        yield np.roll(a, r, 0)


def parse(data):
    scans = [np.genfromtxt(StringIO(s), delimiter=',',
                           dtype=int, skip_header=1)
             for s in data.split("\n\n")]
    return [s[np.lexsort(np.rot90(s))] for s in scans]


def align(scanners):
    remain = list(enumerate(scanners))
    done = [remain.pop(0) + (np.array((0, 0, 0)),)]
    while remain:
        found = False
        for ai, a, _ in done:
            aset = {tuple(p) for p in a}
            for i, (bi, b) in enumerate(remain):
                sz = min(len(b), len(a))
                for bb in perms(b):
                    delta = a[:sz] - bb[:sz]
                    unq, cnt = np.unique(delta, axis=0, return_counts=True)
                    if max(cnt) < 2:
                        continue
                    for j, c in sorted(enumerate(cnt), key=lambda x: x[1]):
                        offset = unq[j]
                        aligned = bb + offset
                        bset = {tuple(p) for p in aligned}
                        common = aset.intersection(bset)
                        if len(common) >= 12:
                            remain.pop(i)
                            done.append((bi, aligned, offset))
                            print(f"{len(done)} done, {len(remain)} remain")
                            found = True
                            break
                    if found:
                        break
            if found:
                break
        if not found:
            print("uh oh, found none on entire iteration, giving up")
            with open('output', 'w') as f:
                f.write(str(remain))
                f.write("\n\n")
                f.write(str(done))
            return None
    return done


def solve(scanners):
    beacons = set()
    positions = list()
    for i, scan, pos in scanners:
        beacons.update({tuple(p) for p in scan})
        positions.append(pos)
    p1 = len(beacons)
    p2 = max([np.abs(a - b).sum() for a in positions for b in positions])
    return p1, p2


if __name__ == "__main__":
    with open('sample') as f:
        sample = f.read().strip()
    scanners = parse(sample)
    print(solve(align(scanners)))

    with open('input') as f:
        data = parse(f.read().strip())
    scanners = align(data)
    print(solve(align(data)))
