#!/usr/bin/env python

sample = [("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""", (10, 36)), ("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""", (19, 103)), ("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""", (226, 3509))]


class Cave:
    def __init__(self, v):
        self.v = v
        self.big = v.isupper()
        self.start = v == 'start'
        self.end = v == 'end'
        self.exits = []

    def __repr__(self):
        return repr(self.v)


class Path:
    def __init__(self, lst=None, full=False):
        self.lst = lst or list()
        self.full = full

    def step(self, e):
        if e.big:
            return Path(self.lst + [e], self.full)
        if e.start:
            return None
        if e not in self.lst:
            return Path(self.lst + [e], self.full)
        if self.full:
            return None
        return Path(self.lst + [e], True)


def parse(cave):
    c = {}
    for p in cave.split("\n"):
        src, dst = map(lambda x: c.setdefault(x, Cave(x)), p.split("-"))
        src.exits.append(dst)
        dst.exits.append(src)
    return c['start']


def pathfind(current, path, count):
    if path:
        for e in current.exits:
            if e.end:
                count[path.full] += 1
            else:
                pathfind(e, path.step(e), count)


def walk(cave):
    count = [0, 0]
    pathfind(parse(cave), Path(), count)
    p1 = count[0]
    p2 = sum(count)
    return p1, p2


if __name__ == "__main__":
    for c, (f1, f2) in sample:
        p1, p2 = walk(c.strip())
        if (p1, p2) != (f1, f2):
            print("Error!", (p1, p2), (f1, f2))
            import sys
            sys.exit(1)
        print("sample", p1, p2)
    with open('input') as f:
        data = f.read().strip()
    print("input", walk(data))
