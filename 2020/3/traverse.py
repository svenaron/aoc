#!/usr/bin/env python3

def traverse(fname, dx, dy):
    path = ""
    x = 0
    y = 0
    with open(fname) as f:
        l = f.readline().strip()
        while l:
            path += l[x % len(l)]
            x += dx
            y += dy
            for _ in range(dy):
                l = f.readline().strip()
    return path

if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    p = traverse(fname, 3, 1)
    print(p.count('#'))

    res = [traverse(fname, x, y).count('#')
           for (x,y) in ((1,1),(3, 1),(5, 1),(7, 1),(1, 2))]
    c = 1
    for r in res:
        c *= r
    print(res)
    print(c)
