#!/usr/bin/env python3
import sys

vert = None
horiz = None
diag1 = None
diag2 = None

def change(room, seat, r, s):
    if seat == '.':
        return '.'
    adj = "".join([row[s - 1 if s > 0 else 0:s + 2]
                   for row in room[r - 1 if r > 0 else 0:r + 2]])
    occupied = adj.count('#')
    if not occupied:
        return '#'
    if occupied > 4:
        return 'L'
    return seat

def inrange(room, r, s):
    return (r >= 0 and r < len(room)
            and s >= 0 and s < len(room[0]))

def look(room, r, s, ds, dr):
    l = '.'
    r += dr
    s += ds
    while l not in "#L" and inrange(room, r, s):
        l = room[r][s]
        r += dr
        s += ds
    return l

def change_seen(room, seat, r, s):
    if seat == '.':
        return '.'
    seen = [look(room, r, s, ds, dr) for
            (ds, dr) in ((0, 1), (0, -1),
                         (1, 0), (-1, 0),
                         (-1, -1), (1, 1),
                         (-1, 1), (1, -1))]
    occupied = seen.count('#')
    if not occupied:
        return '#'
    if occupied > 4:
        return 'L'
    return seat


def move_around(room, fun = change):
    return ["".join([fun(room, seat, r, s) for s, seat in enumerate(row)])
            for r, row in enumerate(room)]

def process(room, fun = change):
    n = move_around(room, fun)
    if n == room:
        return room
    return process(n, fun)

if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        room = f.read().strip().split("\n")
    new_room = "\n".join(process(room))
    print(new_room.count('#'))
    print("===")
    new_room = "\n".join(process(room, change_seen))
    print(new_room.count('#'))
