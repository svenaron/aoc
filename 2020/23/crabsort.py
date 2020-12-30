#!/usr/bin/env python3
import sys

sample = "389125467"
sample_res1 = 92658374
sample_res2 = (934001, 159792)

MAXLEN = 100

def sort(cups):
    current = cups[0]
    move = cups[1:4]
    rest = cups[4:]
    dest = current - 1
    while dest not in rest:
        dest = max(cups) if dest < min(cups) else dest - 1
    return rest[:rest.index(dest)+1] + move + rest[rest.index(dest) + 1:] + (current,)

def get_number(cups):
    num = cups[cups.index(1) + 1:] + cups[:cups.index(1)]
    return int("".join(map(str, num)))

class LL(int):
    nxt = None
    def insert3(self, first):
        last = first.nxt.nxt
        last.nxt = self.nxt
        self.nxt = first
    def remove3(self):
        first = self.nxt
        last = first.nxt.nxt
        self.nxt = last.nxt
        return first

def crabsort(numbers, moves):
    nums = [LL(n) for n in numbers]
    nums += [LL(n) for n in range(10, 1000001)]
    cups = {}
    for a,b in zip(nums, nums[1:] + [nums[0]]):
        a.nxt = b
        cups[a] = a

    mincup = 1
    maxcup = 1000000
    current = nums[0]
    for i in range(moves):
        move = current.remove3()
        dest = maxcup if current == mincup else current - 1
        while dest in [move, move.nxt, move.nxt.nxt]:
            dest = maxcup if dest == mincup else dest - 1
        tgt = cups[dest]
        tgt.insert3(move)
        current = current.nxt
        if i % 1000000 == 0:
            sys.stdout.write(f"\r bigsort2 {int(i / moves * 100)}%")
            sys.stdout.flush()
    sys.stdout.write("\r")
    one = cups[1]
    return (one.nxt, one.nxt.nxt)

def test():
    cups = tuple(map(int, sample))
    for _ in range(10):
        cups = sort(cups)
    p1 = get_number(cups)
    print("test1", p1)
    cups = tuple(map(int, sample))
    import cProfile
    p = cProfile.Profile()
    p2 = p.runcall(crabsort, cups, 10000000)
    p.print_stats()
    print("test2", p2, p2[0] * p2[1])
    return p1 == sample_res1 and p2 == sample_res2

if __name__ == "__main__":
    if not test():
        sys.exit(1)

    cups = tuple(map(int, "389547612"))
    for _ in range(100):
        cups = sort(cups)
    p1 = get_number(cups)
    print("part1", p1)
    cups = tuple(map(int, "389547612"))
    p2 = crabsort(cups, 10000000)
    print("part2", p2, p2[0] * p2[1])
