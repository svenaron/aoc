#!/usr/bin/env python3
import sys, re

rex = r'(.*) bags?'

def rule(line):
    line = re.sub(r'( bags?)|\.', '', line)
    bag, contains = re.split(' contains?', line, 1)
    if "no other" in contains:
        return (bag, {})
    contains = [inner.strip().split(" ", 1) for inner in contains.split(',')]
    return (bag, dict([(color, int(num)) for (num, color) in contains]))

def contains(rules, kind):
    colors = set()
    for k, v in rules.items():
        if kind in v:
            colors.add(k)
            colors.update(contains(rules, k))
    return colors

def count(rules, kind):
    c = 1
    for (color, num) in rules[kind].items():
        c += num * count(rules, color)
    return c

def parse(fname):
    with open(fname) as file:
        rules = dict([rule(l) for l in file])
    return rules

if __name__ == "__main__":
    fname = sys.argv[1]
    rules = parse(fname)
    print(len(contains(rules, 'shiny gold')))
    print(count(rules, 'shiny gold') - 1)
