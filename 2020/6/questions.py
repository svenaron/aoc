#!/usr/bin/env python3
import sys

def group_sum(grp):
    res = {}
    cnt = 0
    for person in grp.split('\n'):
        cnt += 1
        for q in person.strip():
            v = res.get(q, 0)
            res[q] = v + 1
    yes = sum([1 for v in res.values() if v == cnt])
#    print(grp, res, cnt)
#    print("--")
    return yes


def countyes(fname):
    with open(fname) as file:
        groups = file.read().strip().split('\n\n')
        return sum([group_sum(g) for g in groups])


if __name__ == "__main__":
    fname = sys.argv[1]
    print(countyes(fname))
