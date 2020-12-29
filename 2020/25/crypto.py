#!/usr/bin/env python3
import re
import itertools

def transform(value = 1, sn = 7):
    return (value * sn) % 20201227

def encryption_key(subject, loops):
    v = 1
    for _ in range(loops):
        v = transform(v, subject)
    return v

def brute_force_loop_size(keys):
    ret = {}
    i = 0
    v = 1
    for k in sorted(keys):
        while True:
            v = transform(v)
            i += 1
            if v == k:
                ret[v] = i
                break
    return ret

def test():
    sample = (5764801,17807724)
    lsz = brute_force_loop_size(sample)
    subject = sample[1]
    loops = lsz[sample[0]]
    t1 = encryption_key(subject, loops)
    print("Test1", t1)
    return t1 == 14897079

if __name__ == "__main__":
    import sys
    if not test():
        print("Tests FAIL")
        sys.exit(1)
    print("Tests OK")
    data = (3469259, 13170438)
    lsz = brute_force_loop_size(data)
    low, high = sorted(lsz.items(), key = lambda x: x[1])
    loop = low[1]
    subject = high[0]
    p1 = encryption_key(subject, loop)
    print("Part1", p1)
