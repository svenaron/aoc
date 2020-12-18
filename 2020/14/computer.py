#!/usr/bin/env python2
import sys
import re

class MemoryNode:
    def __init__(self, depth):
        self.depth = depth
        self.children = [None, None]
        self.val = 0
    def child(self, b):
        if not self.children[b]:
            self.children[b] = MemoryNode(self.depth + 1)
        return self.children[b]
    def sum(self):
        if any(self.children):
            return sum([x.sum() for x in self.children if x])
        return self.val


class CPU:
    def __init__(self, prog):
        self.prog = prog

    def run(self):
        self.setmask = 0
        self.clrmask = 0
        self.mem = {}
        for cmd, arg in self.prog:
            if cmd == "mask":
                bits = list(enumerate(reversed(arg)))
                self.setmask = sum([1 << i for i, c in bits if c == '1'])
                self.clrmask = sum([1 << i for i, c in bits if c == '0'])
            else:
                val = (int(arg) | self.setmask) & ~(self.clrmask)
                addr = int(cmd.split("[")[1][:-1])
                self.mem[addr] = val

    def run2(self):
        self.setmask = 0
        self.fltmask = []
        self.mem = {}
        self.memnode = MemoryNode(0)
        for cmd, arg in self.prog:
            if cmd == "mask":
                self.mask = arg
                bits = list(enumerate(reversed(arg)))
                self.setmask = sum([1 << i for i, c in bits if c == '1'])
                self.fltmask = [i for i, c in bits if c == 'X']
            else:
                val = int(arg)
                addr = int(cmd.split("[")[1][:-1]) | self.setmask
                #self.write(val, addr, self.fltmask, 0)
                self.write2(val, addr, self.fltmask, 0)

    def write(self, val, addr, mask, i):
        if i < len(mask):
            m = mask[i]
            self.write(val, addr | (1 << m), mask, i+1)
            self.write(val, addr & ~(1 << m), mask, i+1)
        else:
            self.mem[addr] = val

    def write2(self, val, addr, mask, i, node = None):
        if node is None:
            node = self.memnode
        if i < len(mask):
            b = mask[i]
            if b > node.depth:
#                print("depth", i, "bit", b, "unmodified", self.mask)
                bit = (addr >> i) & 1
                self.write2(val, addr, mask, i, node.child(bit))
            else:
#                print("depth", i, "bit", b, "floating", self.mask)
                self.write2(val, addr, mask, i+1, node.child(1))
                self.write2(val, addr, mask, i+1, node.child(0))
        else:
            node.val = val

if __name__ == "__main__":
    fname = sys.argv[1]
    with open(fname) as f:
        prog = list(map(lambda x: x.split(" = "), f.read().strip().split("\n")))
    cpu = CPU(prog)
    cpu.run()
    print(sum(cpu.mem.values()))
    cpu.run2()
    print(sum(cpu.mem.values()))
    print(cpu.memnode.sum())
