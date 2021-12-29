#!/usr/bin/env python

from operator import add, mul, floordiv as div, mod, eq as eql  # noqa
from array import array


def parse(instr):
    r = (instr[0] if instr[0] == 'inp' else eval(instr[0]),)
    return r + tuple(a if a in 'wxyz' else int(a) for a in instr[1:])


def blockwise(prog):
    blocks = []
    for r in prog:
        if r[0] == 'inp':
            blocks.append(list())
        blocks[-1].append(r)
    return blocks


def run(prog):
    state = [[array('q', [0, 0, 0, 0]), (0, 0)]]
    prog = [parse(line.split()) for line in open(prog).readlines()]
    blocks = blockwise(prog)
    for d, block in enumerate(blocks):
        # Each block begins with an input
        inp, a = block[0]
        a = 'wxyz'.index(a)

        # Remove duplicate states
        for s in state:
            s[0][a] = 0
        state.sort()
        i = 0
        for j in range(1, len(state)):
            if state[i][0] == state[j][0]:
                state[i][1] = (min(state[i][1][0], state[j][1][0]),
                               max(state[i][1][1], state[j][1][1]))
            else:
                i += 1
                state[i] = state[j]
        del state[i+1:]

        # Each state branches into 9 new states
        nxt = []
        while state:
            (regs, (lo, hi)) = state.pop()
            for i in range(1, 10):
                nregs = array('q', regs)
                nregs[a] = i
                nhi = lo * 10 + i
                nlo = hi * 10 + i
                nxt.append([nregs, (nlo, nhi)])
            del regs
        del state
        state = nxt
        print(d+1, 'digits', len(state), 'states')

        # Now process the rest of the block for each state
        for regs, _ in state:
            for instr, a, b in block[1:]:
                a = 'wxyz'.index(a)
                regs[a] = instr(regs[a], val(regs, b))

    state = [(lo, hi) for regs, (lo, hi) in state if regs[3] == 0]
    lo = min([lo for (lo, hi) in state])
    hi = max([hi for (lo, hi) in state])
    print("p1", lo)
    print("p2", hi)


def val(regs, v):
    if isinstance(v, int):
        return v
    return regs['wxyz'.index(v)]


if __name__ == "__main__":
    run('input')
