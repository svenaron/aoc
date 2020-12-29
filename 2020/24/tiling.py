#!/usr/bin/env python3
import re
import itertools

delta = {'e': (2, 0), 'w': (-2, 0),
         'se': (1, -1), 'sw': (-1, -1),
         'ne': (1, 1), 'nw': (-1, 1)}

def adjacent(x, y):
    return {(x + dx, y + dy) for (dx, dy) in delta.values()}

def flip(black):
    white = set(itertools.chain(*[adjacent(*t).difference(black) for t in black]))
    flip_to_black = {t for t in white
                     if len(black.intersection(adjacent(*t))) == 2}
    flip_to_white = {t for t in black
                     if len((black - {t}).intersection(adjacent(*t))) not in [1, 2]}
    return (black - flip_to_white).union(flip_to_black)

def parse(data):
    directions = data.strip().split('\n')
    black = set()
    for line in directions:
        steps = [delta[s] for s in re.findall(r'(e|w|se|sw|ne|nw)', line)]
        tile = tuple([sum(i) for i in zip(*steps)])
        try:
            black.remove(tile)
        except KeyError:
            black.add(tile)
    return black

def test():
    with open('sample') as f:
        sample = f.read()
    tiles = parse(sample)
    t1 = len(tiles)
    print("test1", t1)
    for i in range(100):
        tiles = flip(tiles)
    t2 = len(tiles)
    print("test2", t2)
    return t1 == 10 and t2 == 2208

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    print("Tests OK")
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read().strip()
            tiles = parse(data)
            p1 = len(tiles)
            print("part1", p1)
            for _ in range(100):
                tiles = flip(tiles)
            p2 = len(tiles)
            print("part2", p2)
