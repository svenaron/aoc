#!/usr/bin/env python3
import re
one = 0
two = 0
with open('input') as f:
    line = f.readline()
    while line:
        rule, password = map(lambda x: x.strip(), line.split(':'))
        interval, character = rule.split()
        low, high = map(int, interval.split('-'))
        c = password.count(character)
        if (c >= low and c <= high):
            one += 1
        a = password[low-1] == character
        b = password[high-1] == character
        if (a ^ b):
            two += 1

        line = f.readline()
print("one", one)
print("two", two)
