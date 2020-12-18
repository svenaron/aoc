#!/usr/bin/env python3
import sys, re

class cpu:
    acc = 0
    pc = 0
    trace = None
    patched = False
    def __init__(self, fname):
        self.trace = list()
        with open(fname) as file:
            self.prog = list(map(lambda x: x.split(), file.read().strip().split('\n')))

    def step(self):
        if self.pc < len(self.prog):
            cmd, arg = self.prog[self.pc]
            nxt = self.pc + 1
            if cmd == 'nop':
                pass
            elif cmd == 'acc':
                self.acc += int(arg)
            elif cmd == 'jmp':
                nxt = self.pc + int(arg)
            else:
                raise Exception(f"invalid instruction {cmd} {arg}")
            self.trace.append(self.pc)
            self.pc = nxt

    def nextcmd(self):
        return self.prog[self.pc].split()[0]

    def patch(self, tried):
        if not self.patched and self.pc not in tried:
            if self.prog[self.pc][0] in ['jmp', 'nop']:
                cmd = 'jmp' if self.prog[self.pc][0] == 'nop' else 'nop'
                self.prog[self.pc][0] = cmd
                tried.append(self.pc)
                self.patched = True


def run(fname, limit):
    m = cpu(fname)
    while m.pc not in m.trace:
        m.step()
    print(m.acc)
    tried = []
    while m.pc < len(m.prog):
        m = cpu(fname)
        while m.pc not in m.trace and m.pc < len(m.prog):
            m.patch(tried)
            m.step()
    print(m.pc, len(m.prog), m.acc)

if __name__ == "__main__":
    fname = sys.argv[1]
    run(fname, 1)
