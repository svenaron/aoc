#!/usr/bin/env python3
import re

sample = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def parse(data):
    data = re.sub('[,()]', '', data)
    meals = [(set(f.split()), set(a.split()))
             for (f, a) in [l.split('contains') for l in data.split('\n')]]
    all_food = set()
    all_allergens = set()
    for (f, a) in meals:
        all_food.update(f)
        all_allergens.update(a)

    may_contain = {}
    for (f, allergens) in meals:
        for a in allergens:
            s = may_contain.setdefault(a, set(f))
            for (ff, aa) in meals:
                if a in aa:
                    s.intersection_update(ff)

    badfood = set()
    badfood.update(*may_contain.values())
    safe_food = all_food - badfood
    count = 0
    for sf in safe_food:
        for f, a in meals:
            if sf in f:
                count += 1
    while any([len(f) > 1 for f in may_contain.values()]):
        for a, f in may_contain.items():
            if len(f) == 1:
                for aa, ff in may_contain.items():
                    if aa != a:
                        ff.difference_update(f)
    ilist = sorted(may_contain.items())
    return count, ",".join([f.pop() for (a, f) in ilist])

def test():
    r, l = parse(sample.strip())
    print("test1", r)
    print("test2", l)
    return r == 5 and l == 'mxmxvkd,sqjhc,fvjkl'

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read().strip()
            p1, p2 = parse(data)
            print("part1", p1)
            print("part2", p2)
