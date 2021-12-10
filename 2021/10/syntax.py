#!/usr/bin/env python

sample="""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

match = {'(': ')',
         '{': '}',
         '<': '>',
         '[': ']'}

err = {')': 3,
       ']': 57,
       '}': 1197,
       '>': 25137}

tail = {')': 1,
        ']': 2,
        '}': 3,
        '>': 4,}

def check(line):
    stack = []
    for l in line:
        if l in match:
            stack.append(match[l])
        else:
            c = stack.pop()
            if c != l:
                return (err[l], 0)
    r = 0
    for c in reversed(stack):
        r = r * 5 + tail[c]
    return (0, r)

def score(data, p1=False, p2=False):
    for line in data:
        e, r = check(line)
        if p1 and e:
            yield(e)
        if p2 and r:
            yield(r)

def syntax(data):
    p1 = sum(score(data, p1=True))
    p2 = sorted(score(data, p2=True))
    p2 = p2[len(p2) // 2]
    return p1, p2

if __name__ == "__main__":
    print("sample", syntax(sample.split("\n")))
    with open('input') as f:
        data = f.read().strip().split('\n')
    print("input", syntax(data))
