#!/usr/bin/env python

import numpy as np

sample = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def bingo(data):
    numbers, *boards = data.split("\n\n")
    boards = [np.array([list(map(int, l.split())) for l in b.split('\n')])
              for b in boards]
    winning = []
    for n in map(int, numbers.split(',')):
        for i, b in enumerate(boards):
            if b is None:
                continue
            b = np.where(b==n, -1, b)
            score = np.concatenate((np.sum(b, 0), np.sum(b, 1)))
            if -5 in score:
                winning.append(np.sum(np.where(b==-1, 0, b)) * n)
                boards[i] = None
            else:
                boards[i] = b
    return (winning[0], winning[-1])


if __name__ == "__main__":
    print(bingo(sample))
    with open('input') as f:
        data = f.read().strip()
    print(bingo(data))
