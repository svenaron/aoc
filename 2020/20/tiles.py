#!/usr/bin/env python3
import math
import re

sample_grid = [[1951, 2311, 3079],
               [2729, 1427, 2473],
               [2971, 1489, 1171]]
sample_sum = 20899048083289

sea_monster = [r"                  # ",
               r"#    ##    ##    ###",
               r" #  #  #  #  #  #   "]
sea_rex = [x.replace(' ', '.') for x in sea_monster]
hashes_in_monster = "".join(sea_monster).count('#')

WEST = 1
EAST = -WEST
NORTH = 2
SOUTH = -NORTH

class Tile:
    def __init__(self, data = None, num = None, tile = None,
                 rotation = 0, flip = 0):
        """Initialize with raw data or num and tile. Rotation and flip is just
           for representation"""
        if num and tile:
            self.num = num
            self.tile = tile
        else:
            title, tile = data.split(':')
            self.num = int(title.split()[1])
            self.tile = tuple([tuple(x) for x in tile.strip().split('\n')])
        self.edges = {WEST:  tuple((r[0] for r in self.tile)),
                      EAST:  tuple((r[-1] for r in self.tile)),
                      NORTH: self.tile[0],
                      SOUTH: self.tile[-1]}
        self.exits = {}
        self.rotation = rotation
        self.flip = flip

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
        """Returns True if edge in 'direction' aligns with other"""
        if self.num == other.num:
            return False
        return self.edges[direction] == other.edges[-direction]

    def set_exits(self, edict):
        """Find the matching tile, if any, for all edges"""
        for d in self.edges:
            r = {t for t in edict[self.edges[d]] if self.aligns(t, d)}
            self.exits[d] = r.pop() if r else None

    def rotated(self, n = 1):
        """Return this tile rotated n steps"""
        for _ in range(n):
            tile = tuple(rotate(self.tile))
        return Tile(num = self.num, tile = tile,
                    rotation = self.rotation + n, flip = self.flip)

    def flipped(self):
        """Return this tile flipped horizontally"""
        tile = list(reversed(self.tile))
        return Tile(num = self.num, tile = tile,
                    rotation = self.rotation, flip = 0 if self.flip else 1)

def rotate(grid):
    return zip(*grid[::-1])

def parse(data):
    data = data.split('\n\n')
    tiles = [Tile(d) for d in data]

    # Create all variant tiles
    variants = set()
    for t in tiles:
        for _ in range(2):
            t = t.flipped()
            for _ in range(4):
                t = t.rotated()
                variants.add(t)

    # Create an edge-dictionary of all variant edges
    vdict = {}
    for t in variants:
        for e in t.edges.values():
            vdict.setdefault(e, set()).add(t)
    # Set the exits of all variant tiles
    for t in variants:
        t.set_exits(vdict)

    # Find the corners
    corners = {v.num for v in variants if
               sum([bool(e) for e in v.exits.values()]) == 2}

    part1 = 1
    for c in corners:
        part1 *= c

    # Find all variant NW corners
    nwc = [v for v in variants
           if v.num in corners
           and v.exits[NORTH] is None
           and v.exits[WEST] is None]

    # Pick one NW corner and trace it to build a grid
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

    # Collect all lines to build the image
    image = []
    for row in grid:
        for i in range(1, 9):
            rr = ""
            for t in row:
                rr += t.get_line(i)
            image.append(rr)

    # Rotate and flip the image while looking for monsters
    img = list(map(tuple, image))
    mc = (0, None)
    for _ in range(2):
        img = list(reversed(img))
        for _ in range(4):
            img = ["".join(x) for x in rotate(img)]
            c = find_monsters(img)
            if c > mc[0]:
                mc = (c, img)

    # Count the number of '#' and subtract all monster-'#'
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
    part1, part2 = parse(data)
    print("test1", part1)
    print("test2", part2)
    return part1 == 20899048083289 and part2 == 273

if __name__ == "__main__":
    import sys
    if not test():
        sys.exit(1)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read().strip()
            part1, part2 = parse(data)
            print("part1", part1)
            print("part2", part2)
