#!/usr/bin/env python

def testrange(xx, yy):
    return ((x, y)
            for x in range(1, max(xx) + 1)
            for y in range(min(yy), abs(min(yy)) + 1))

def test(dx, dy, xx, yy):
    x, y = (0, 0)
    my = 0
    v = (dy, dx)
    while x <= xx[1] and y >= yy[1]:
        x += dx
        y += dy
        dx = dx - 1 if dx else 0
        dy -= 1
        if dy == 0:
            my = y
        if x >= xx[0] and x <= xx[1] and y <= yy[0] and y >= yy[1]:
            return (my, v)
    return (None, v)

def probe(xx, yy):
    res = (test(x, y, xx, yy) for x, y in testrange(xx, yy))
    ontarget = [r for r in res if r[0] is not None]
    p1 = max(r[0] for r in ontarget)
    p2 = len(set((x, y) for s, (x, y) in ontarget))
    return p1, p2

if __name__ == "__main__":
    xx, yy = ((20, 30), (-5, -10))
    p1, p2 = probe(xx, yy)
    print("sample", p1, p2)

    xx, yy = ((117, 164), (-89, -140))
    p1, p2 = probe(xx, yy)
    print("input", p1, p2)
