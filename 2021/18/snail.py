#!/usr/bin/env python

import re

lrex = re.compile(r'(\d+)([^\d]+)$')
rrex = re.compile(r'(\d+)')
srex = re.compile(r'(\d\d+)')
nrex = re.compile(r'\[(\d+),(\d+)\]')


def addleft(expr, n):
    mob = lrex.search(expr)
    if mob:
        r = int(mob.group(1))+n
        return lrex.sub(rf'{r}\2', expr, 1)
    return expr


def addright(expr, n):
    mob = rrex.search(expr)
    if mob:
        return rrex.sub(rf'{int(mob.group(1))+n}', expr, 1)
    return expr


def reduce(expr):
    while True:
        depth = 0
        i = 0
        while i < len(expr):
            c = expr[i]
            if c == ',':
                pass
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
            elif depth > 4:
                num = nrex.search(expr[i-1:])
                a, b = map(int, num.groups())
                l = expr[:num.span()[0]+i-1]
                r = expr[num.span()[1]+i-1:]
                left = addleft(l, a)
                right = addright(r, b)
                expr = left + "0" + right
                i = len(left)
                depth -= 1
                continue
            i += 1

        mob = srex.search(expr)
        if not mob:
            break

        n = int(mob.group(1))
        a, b = (n // 2,  (n+1) // 2)
        expr = expr[:mob.span()[0]] + f'[{a},{b}]' + expr[mob.span()[1]:]
    return expr


def solve1(expressions):
    res = expressions[0]
    for e in expressions[1:]:
        res = reduce(f'[{res},{e}]')
    return mag(eval(res))


def mag(x):
    if isinstance(x, int):
        return x
    return 3 * mag(x[0]) + 2 * mag(x[1])


def solve2(expressions):
    res = 0
    for a in expressions:
        for b in expressions:
            if a == b:
                continue
            r = solve1([a, b])
            if r > res:
                res = r
    return res

if __name__ == "__main__":
    with open('input') as f:
        data = f.read().strip().split("\n")
    print(solve1(data))
    print(solve2(data))
