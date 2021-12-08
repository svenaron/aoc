#!/usr/bin/env python

from itertools import permutations

sample = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

key = {"abcefg" : "0",
       "cf"     : "1",
       "acdeg"  : "2",
       "acdfg"  : "3",
       "bcdf"   : "4",
       "abdfg"  : "5",
       "abdefg" : "6",
       "acf"    : "7",
       "abcdefg": "8",
       "abcdfg" : "9", }

perms = set(permutations("abcdefg"))

def test(wiring, txl):
    options = dict(key)
    for digit in sorted(wiring, key=len):
        d = "".join(sorted([txl[d] for d in digit]))
        try:
            options.pop(d)
        except KeyError:
            return False
    return True

def translate(output, txl):
    r = ""
    for digit in output:
        d = "".join(sorted([txl[d] for d in digit]))
        r += key[d]
    return int(r)

def findnumber(wiring, output):
    for p in perms:
        txl = {k: v for k,v in zip("abcdefg", p)}
        if test(wiring, txl):
            return translate(output, txl)

def search(data):
    data = [e.split(' | ') for e in data.split("\n")]
    data = [(w.split(), o.split()) for (w, o) in data]
    p1 = [[x for x in output if len(x) in (2,3,4,7)]
          for wiring, output in data]
    p1 = sum([len(x) for x in p1])
    p2 = [findnumber(*d) for d in data]
    return p1, sum(p2)

if __name__ == "__main__":
    print("sample", search(sample))
    with open('input') as f:
        data = f.read().strip()
    print("input", search(data))
