#!/usr/bin/env python3
import copy

sample = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

def combat(d1, d2, recursive = False):
    history = set()
    while d1 and d2:
        p1_wins = d1[0] > d2[0]

        if recursive:
            if (d1, d2) in history:
                return (True, d1)
            history.add((d1, d2))
            if len(d1) > d1[0] and len(d2) > d2[0]:
                p1_wins, _ = combat(d1[1:d1[0] + 1], d2[1:d2[0] + 1], True)

        if p1_wins:
            d1 = d1[1:] + (d1[0], d2[0])
            d2 = d2[1:]
        else:
            d2 = d2[1:] + (d2[0], d1[0])
            d1 = d1[1:]

    return (bool(d1), d1 or d2)

def score(deck):
    return sum([(i+1) * card for i, card in enumerate(reversed(deck))])

def parse(data):
    cards = data.strip().split('\n\n')
    cards = [[int(x) for x in deck.split(':')[1].split('\n') if x]
             for deck in cards]
    p1, p2 = cards
    _, deck1 = combat(tuple(p1), tuple(p2), False)
    _, deck2 = combat(tuple(p1), tuple(p2), True)
    part1 = score(deck1)
    part2 = score(deck2)
    return (part1, part2)

def test():
    r, l = parse(sample.strip())
    print("test1", r)
    print("test2", l)
    return True

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
