import sys

with open(sys.argv[1]) as f:
    prog = f.read().strip().split("\n")

print("""
void monad(int d, long long int* regs) {
    long long int w = regs[0], x = regs[1], y = regs[2], z = regs[3];
    switch(d) {
""")
d = 0
ops = {'mul': '*', 'add': '+', 'div': '/', 'mod': '%'}
for p in prog:
    if 'inp' in p:
        if d > 0:
            print("        break;")
        print(f"    case {d}:")
        d += 1
    else:
        op, a, b = p.split()
        if op == 'eql':
            print(f"        {a} = {a} == {b};")
        else:
            print(f"        {a} {ops[op]}= {b};")
print("        break;")
print("""
        default:
    }
    regs[0] = w;
    regs[1] = x;
    regs[2] = y;
    regs[3] = z;
}""")
