#!/usr/bin/env python
# no-fisketur

from io import StringIO
import numpy as np
from operator import lt, gt, eq

txl = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

sample = [("38006F45291200", 9),
          ("EE00D40C823060", 14),
          ("8A004A801A8002F478", 16),
          ("620080001611562C8802118E34", 12),
          ("C0015000016115A2E0802F182340", 23),
          ("A0016C880162017C3686B18A3D4780", 31)]


ops = {
    0: lambda packets: sum(ops[p[1]](p[2]) for p in packets),
    1: lambda packets: np.prod([ops[p[1]](p[2]) for p in packets]),
    2: lambda packets: min(ops[p[1]](p[2]) for p in packets),
    3: lambda packets: max(ops[p[1]](p[2]) for p in packets),
    4: lambda lvalue: int(lvalue, 2),
    5: lambda packets: gt(*(ops[p[1]](p[2]) for p in packets)),
    6: lambda packets: lt(*(ops[p[1]](p[2]) for p in packets)),
    7: lambda packets: eq(*(ops[p[1]](p[2]) for p in packets)),
}


def lvalue(data):
    e = data.read(1)
    return data.read(4) + (lvalue(data) if e == '1' else '')


def operator(data):
    if data.read(1) == '0':
        cnt = int(data.read(15), 2)
        return subpackets(StringIO(data.read(cnt)))
    else:
        cnt = int(data.read(11), 2)
        return [packet(data) for _ in range(cnt)]


def packet(data, v=None):
    v = int(v or data.read(3), 2)
    t = int(data.read(3), 2)
    p = lvalue(data) if t == 4 else operator(data)
    return (v, t, p)


def subpackets(data):
    r = []
    while len(version := data.read(3)) == 3:
        r.append(packet(data, version))
    return r


def parse(data):
    return StringIO("".join(txl[c] for c in data))


def sumversion(packets):
    r = np.sum([[v, sumversion(p if isinstance(p, list) else [])]
                for (v, t, p) in packets])
    return int(r)


def peval(p):
    return ops[p[1]](p[2])


if __name__ == "__main__":
    for c, f1 in sample:
        data = parse(c)
        p = packet(data)
        p1 = sumversion([p])
        p2 = peval(p)
        print("sample", p1, f1, p2)
        assert(p1 == f1)

    with open('input') as f:
        data = parse(f.read().strip())
    p = packet(data)
    p1 = sumversion([p])
    p2 = peval(p)
    print("input", p1, p2)
