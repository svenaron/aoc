#!/usr/bin/env python3
import math
import re

sample_grid = [[1951, 2311, 3079],
               [2729, 1427, 2473],
               [2971, 1489, 1171]]
sample_sum = 20899048083289

WEST  = (-1,  0)
EAST  = ( 1,  0)
NORTH = ( 0, -1)
SOUTH = ( 0,  1)

sea_monster = [r"                  # ",
               r"#    ##    ##    ###",
               r" #  #  #  #  #  #   "]
sea_rex = [x.replace(' ', '.') for x in sea_monster]
hashes_in_monster = "".join(sea_monster).count('#')

class Tile:
    def __init__(self, data = None, num = None, tile = None,
                 rotation = 0, flip = 0):
        if num and tile:
            self.num = num
            self.tile = tile
        else:
            title, tile = data.split(':')
            self.num = int(title.split()[1])
            self.tile = tuple([tuple(x) for x in tile.strip().split('\n')])
        self.rotation = rotation
        self.flip = flip
        self.exits = {}
        self.edges = {WEST:  tuple((r[0] for r in self.tile)),
                      EAST:  tuple((r[-1] for r in self.tile)),
                      NORTH: self.tile[0],
                      SOUTH: self.tile[-1]}

    def __repr__(self):
        return f"<Tile {self.num}:{self.flip}.{self.rotation}>"

    def __hash__(self):
        return hash(self.tile)

    def __eq__(self, other):
        return self.tile == getattr(other, 'tile', None)

    def get_line(self, i):
        """Return line i, without borders"""
        return "".join(self.tile[i][1:-1])

    def all_variant_edges(self):
        """Return all edges this Tile can have"""
        r = set(self.edges.values())
        r.update({tuple(reversed(e)) for e in r})
        return r

    def aligns(self, other, direction):
        """Returns true if this tile aligns with other in 'direction'"""
        if self.num == other.num:
            return False
        reverse = (-direction[0], -direction[1])
        return self.edges[direction] == other.edges[reverse]

    def set_exits(self, edict):
        self.exits = {}
        for d in self.edges:
            r = {t for t in edict[self.edges[d]]
                 if self.aligns(t, d)}
            assert(len(r) in [0, 1])
            self.exits[d] = r.pop() if r else None

    def rotated(self, n = 1):
        for _ in range(n):
            tile = tuple(zip(*self.tile[::-1]))
        return Tile(num = self.num, tile = tile,
                    rotation = self.rotation + n, flip = self.flip)

    def flipped(self):
        tile = list(reversed(self.tile))
        return Tile(num = self.num, tile = tile,
                    rotation = self.rotation, flip = 0 if self.flip else 1)

def corner_key(t):
    r = 's' if t.exits[SOUTH] is None else 'n'
    r += 'w' if t.exits[WEST] is None else 'e'
    return r

def parse(data):
    data = data.split('\n\n')
    tiles = [Tile(d) for d in data]
    edict = {}
    for t in tiles:
        for e in t.all_variant_edges():
            edict.setdefault(e, set()).add(t)

    corners = [t for t in tiles
               if len([e for e in t.edges.values()
                       if len(edict[e]) == 1]) == 2]
    part1 = 1
    for c in corners:
        part1 *= c.num

    # add all variant tiles
    variants = set(tiles)
    for t in tiles:
        for _ in range(2):
            t = t.flipped()
            for _ in range(4):
                t = t.rotated()
                variants.add(t)

    # create an edge-dictionary of all variant edges
    vdict = {}
    for t in variants:
        for e in t.edges.values():
            vdict.setdefault(e, set()).add(t)
    # set the exits of all variants
    for t in variants:
        t.set_exits(vdict)

    nwc = [v for v in variants
           if v.num in [c.num for c in corners]
           and corner_key(v) == 'nw']
    nwc.sort(key = lambda x: repr(x))
    # pick one variant and trace it
    tile = nwc[0]
    dim = int(math.sqrt(len(tiles)))
    grid = [[None] * dim for _ in range(dim)]
    grid[0][0] = tile
    for y in range(dim):
        for x in range(dim):
            if (x, y) == (0, 0):
                continue
            if x == 0:
                grid[y][x] = grid[y-1][x].exits[SOUTH]
            else:
                grid[y][x] = grid[y][x-1].exits[EAST]
    image = []
    for row in grid:
        for i in range(1, 9):
            rr = ""
            for t in row:
                rr += t.get_line(i)
            image.append(rr)

    img = list(map(tuple, image))
    mc = (0, None)
    for _ in range(2):
        img = list(reversed(img))
        for _ in range(4):
            img = ["".join(x) for x in (zip(*img[::-1]))]
            c = find_monsters(img)
            if c > mc[0]:
                mc = (c, img)
    part2 = "".join(mc[1]).count('#') - mc[0] * hashes_in_monster
    return part1, part2

def find_monsters(image):
    c = 0
    for lines in zip(image, image[1:], image[2:]):
        for i in range(len(lines[0]) - len(sea_rex[0])):
            if all([re.match(rex, l[i:])
                    for rex, l in zip(sea_rex, lines)]):
                c += 1
    return c

def test():
    with open('sample') as f:
        data = f.read()
        print("test", parse(data))
    return True

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read().strip()
            part1, part2 = parse(data)
            print("part1", part1)
            print("part1", part2)
