#!/usr/bin/env python3
with open('input') as f:
    numbers = list(map(int, f.readlines()))

print(len(numbers))
for a in numbers:
    for b in numbers:
        for c in numbers:
            if a+b+c == 2020:
                print(a*b*c)
                import sys
                sys.exit(0)
