#!/usr/bin/env python3
import re
import itertools

sample = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".strip()

class Node:
    seed = None
    def __init__(self, data):
        num, rules = data.split(':')
        self.num = int(num)
        if '"' in rules:
            self.path = rules.strip()[1]
        else:
            self.path = [[int(a) for a in r.split()]
                         for r in rules.split('|')]
        self.rules = rules

    def get_regex(self):
        if isinstance(self.path, list):
            subrex = [r"".join(["(?:%s)" % p.get_regex() for p in altpath])
                      for altpath in self.path]
            subrex = ["%s" % s for s in subrex]
            return r"|".join(subrex)
        else:
            return self.path

def tailsearch(substr, rex):
    for i in reversed(range(len(substr))):
        mob = rex.match(substr, i)
        if mob:
            return mob
    return None

def check(substr, r1, r2):
    while substr:
        m1 = r1.match(substr)
        if not m1:
            return False
        substr = substr[m1.span()[1]:]
        m2 = tailsearch(substr, r2)
        if not m2:
            return False
        substr = substr[:m2.span()[0]]
    return True

def parse(data, part2 = False):
    nodes, messages = data.strip().split("\n\n")
    nodes = {int(n.split(':')[0]): Node(n) for n in nodes.split('\n')}
    for n in nodes.values():
        if isinstance(n.path, list):
            n.path = [[nodes[n] if isinstance(n, int) else n for n in p]
                      for p in n.path]
    messages = messages.split('\n')
    if not part2:
        rex = re.compile(nodes[0].get_regex())
        return sum([1 for m in messages if rex.fullmatch(m)])
    else:
        # Rules have changed:
        # 0: 8 11
        # 8: 42 | 42 8
        # 11: 42 31 | 42 11 31
        # This means (42)+(42){x}(31){x}
        # i.e. any number of '42' followed by an equal number of 42 and 31
        n42 = re.compile(nodes[42].get_regex())
        n31 = re.compile(nodes[31].get_regex())
        s = 0
        for msg in messages:
            mob = n42.match(msg)
            if not mob:
                continue
            msg = msg[mob.span()[1]:]
            while msg:
                if check(msg, n42, n31):
                    s += 1
                    break
                mob = n42.match(msg)
                if not mob:
                    break
                msg = msg[mob.span()[1]:]
        return s

def test():
    print("test", parse(sample))
    return True

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read()
            print("part1", parse(data))
            print("part2", parse(data, True))
