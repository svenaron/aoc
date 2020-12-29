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

class LinkedList:
    def __init__(self, lst, prv = None, nxt = None):
        self.lst = list(lst)
        self.prv = prv
        self.nxt = nxt

    def insert_after(self, val, sublist, cache):
        n = self.lst.index(val)
        left = self.lst[:n + 1]
        right = self.lst[n + 1:]
        self.lst = left + sublist + right
        for v in sublist:
            cache[v] = self
        if len(self.lst) > MAXLEN:
            self.splitme(cache)

    def splitme(self, cache):
        newlst = LinkedList(self.lst[MAXLEN:])
        newlst.nxt = self.nxt
        if newlst.nxt:
            newlst.nxt.prev = newlst
        self.nxt = newlst
        self.lst = self.lst[:MAXLEN]
        for v in newlst.lst:
            cache[v] = newlst

    def remove(self, n = 4):
        ret = []
        tgt = self
        while n:
            popped = tgt.lst[:n]
            tgt.lst = tgt.lst[n:]
            n -= len(popped)
            ret += popped
            tgt = tgt.nxt
        return ret

    def append(self, v, cache):
        tgt = self
        while tgt.nxt:
            tgt = tgt.nxt
        if len(tgt.lst) < MAXLEN:
            tgt.lst.append(v)
        else:
            tgt.nxt = LinkedList([v], tgt)
            tgt = tgt.nxt
        cache[v] = tgt


def bigsort(numbers, moves):
    step = 100
    lists = [LinkedList(range(1 + x * step, 1 + x * step + step))
             for x in range(1000000 // step)]
    cache = {}
    for i, sublist in enumerate(lists):
        if (i + 1) < len(lists):
            sublist.nxt = lists[i + 1]
        if i > 1:
            sublist.prv = lists[i - 1]
        for c in sublist.lst:
            cache[c] = sublist

    mincup = 1
    first = lists[0]
    first.lst[0:len(numbers)] = numbers
    last =  lists[-1]
    maxcup = last.lst[-1]

    for i in range(moves):
        move = first.remove(4)
        if not first.lst:
            first = first.nxt
        current = move.pop(0)
        last.append(current, cache)
        dest = maxcup if current == mincup else current - 1
        while dest in move:
            dest = maxcup if dest == mincup else dest - 1
        ll = cache[dest]
        ll.insert_after(dest, move, cache)
        if last.nxt:
            last = last.nxt
        if i % 1000000 == 0:
            sys.stdout.write(f"\r bigsort {int(i / moves * 100)}%")
            sys.stdout.flush()
    sys.stdout.write("\r")

    res = cache[1].lst
    i = res.index(1)
    return (res[i + 1], res[i + 2])

def test():
    cups = tuple(map(int, sample))
    for _ in range(10):
        cups = sort(cups)
    p1 = get_number(cups)
    print("test1", p1)
    cups = tuple(map(int, sample))
    p2 = bigsort(cups, 10000000)
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
    p2 = bigsort(cups, 10000000)
    print("part2", p2, p2[0] * p2[1])
