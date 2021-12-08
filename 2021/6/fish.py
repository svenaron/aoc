#!/usr/bin/env python

sample = "3,4,3,1,2"


def fish(data):
    nums = list(map(int, data.split(',')))
    mature = {i: nums.count(i) for i in range(8)}
    young = {}
    for i in range(256):
        if i == 80:
            p1 = sum(young.values()) + sum(mature.values())
        young[i + 2] = mature[i % 7]
        mature[i % 7] += young.pop(i, 0)
    p2 = sum(young.values()) + sum(mature.values())
    return (p1, p2)


if __name__ == "__main__":
    print(fish(sample))
    with open('input') as f:
        data = f.read().strip()
    print(fish(data))
