#!/usr/bin/env python3
import array

def count(numbers, cnt):
    index = array.array('I', [0] * cnt)
    for i, n in enumerate(numbers[:-1]):
        index[n] = i + 1
    n = numbers[-1]
    for i in range(len(numbers), cnt):
        if index[n]:
            nn = i - index[n]
        else:
            nn = 0
        index[n] = i
        n = nn
    return n

if __name__ == "__main__":
    numbers = [0,5,4,1,10,14,7]
    print(count(numbers, 2020))
    print(count(numbers, 30000000))
