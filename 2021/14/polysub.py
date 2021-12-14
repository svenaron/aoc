#!/usr/bin/env python

from collections import defaultdict

sample = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def parse(data):
    template, rest = data.split("\n\n")
    formula = {i[:2]: i[-1] for i in rest.split("\n")}
    return template, formula


def step(template, formula, n):
    pairs = {a + b: template.count(a + b) for
             (a, b) in zip(template, template[1:])}
    freq = defaultdict(int, {k: template.count(k) for k in set(template)})

    for _ in range(n):
        new_pairs = defaultdict(int)
        for k, v in pairs.items():
            new_pairs[k[0] + formula[k]] += v
            new_pairs[formula[k] + k[1]] += v
            freq[formula[k]] += v
        pairs = new_pairs

    return max(freq.values()) - min(freq.values())


if __name__ == "__main__":
    template, formula = parse(sample)
    s1 = step(template, formula, 10)
    s2 = step(template, formula, 40)
    print("sample1", s1, "INVALID" if s1 != 1588 else "")
    print("sample2", s2, "INVALID" if s2 != 2188189693529 else "")

    with open('input') as f:
        data = f.read().strip()
    template, formula = parse(data)
    print("part1", step(template, formula, 10))
    print("part2", step(template, formula, 40))
