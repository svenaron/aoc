#!/usr/bin/env python3
import sys

class Range:
    def __init__(self, limit):
        self.limit = tuple(limit)
    def valid(self, n):
        return n <= self.limit[1] and n >= self.limit[0]

class Field:
    def __init__(self, data):
        self.name, rule = data.split(":")
        self.ranges = [Range(map(int, r.split('-'))) for r in rule.split('or')]

    def valid(self, n):
        for r in self.ranges:
            if r.valid(n):
                return True
        return False

class Ticket:
    def __init__(self, numbers, fields):
        self.numbers = tuple(numbers)
        self.fields = fields
        self.errors = []
        for n in self.numbers:
            valid = False
            for f in fields:
                if f.valid(n):
                    valid = True
                    break
            if not valid:
                self.errors.append(n)

def check_index(tickets, field, idx):
    for t in tickets:
        if not field.valid(t.numbers[idx]):
            return False
    return True

def find_fields(tickets):
    fields = tickets[0].fields
    rest = {f: set() for f in fields}
    for f in fields:
        for i in range(len(fields)):
            if check_index(tickets, f, i):
                rest[f].add(i)

    done = {}
    while len(done) < len(fields):
        new_done = {f: v.pop() for f,v in rest.items() if len(v) == 1}
        if not new_done:
            print("infinite loop, breaking")
        done.update(new_done)
        rest = {f: v for f, v in rest.items() if f not in done}
        for i in done.values():
            for a, p in rest.items():
                if i in p:
                    p.remove(i)
    return done


if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        rules, mine, others = f.read().strip().split("\n\n")

    others = others.split(':\n')[1].split('\n')
    fields = [Field(r) for r in rules.split('\n')]
    tickets = [Ticket(map(int, o.split(',')), fields) for o in others]
    myticket = Ticket(map(int, mine.split(':')[1].split(',')), fields)
    print("errsum", sum([sum(t.errors) for t in tickets]))
    valid = [t for t in tickets + [myticket] if not t.errors]
    res = 1
    for k, v in find_fields(valid).items():
        if k.name.startswith('departure'):
            res *= myticket.numbers[v]
    print("departure product", res)
