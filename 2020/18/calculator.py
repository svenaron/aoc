#!/usr/bin/env python3
import re

precedence = [["+*"], ["+", "*"]]

samples = [
    ["2 * 3 + (4 * 5)", 26, 46],
    ["5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445],
    ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060],
    ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340],
]

def find(needles, haystack):
    return sorted([haystack.index(n) for n in needles if n in haystack])

def eval1(expr, prec):
    items = list(filter(bool, re.split(r'(?=[*+-/])| ', expr)))
    for ops in prec:
        idx = find(ops, items)
        while idx:
            i = idx.pop(0) - 1
            l = items.pop(i)
            op = items.pop(i)
            r = items.pop(i)
            items.insert(i, str(eval(f'{l} {op} {r}')))
            idx = find(ops, items)
    return str(items[0])

def parse(expr, part):
    p = precedence[part - 1]
    rex = re.compile(r'\(([^()]+)\)')
    while re.search(rex, expr):
        expr = re.sub(rex, lambda x: eval1(x.group(1), p), expr)
    expr = eval1(expr, p)
    return eval(expr)

def test():
    for e, r1, r2 in samples:
        pp1 = parse(e, 1)
        pp2 = parse(e, 2)
        if pp1 != r1:
            print("error pp", pp1, r1)
            return False
        if pp2 != r2:
            print("error pp", pp2, r2)
            return False
    return True

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            expressions = f.readlines()
        s1 = sum([parse(e, 1) for e in expressions])
        s2 = sum([parse(e, 2) for e in expressions])
        print(s1)
        print(s2)
