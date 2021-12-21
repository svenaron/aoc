#!/usr/bin/env python

def parse(data):
    data = data.replace('.', '0').replace('#', '1')
    algo, imagedata = data.split("\n\n")
    image = dict()
    for a, line in enumerate(imagedata.split("\n")):
        for b, char in enumerate(line):
            image[(a, b)] = char
    return image, algo

def points(image):
    xs = [p[0] for p in image]
    ys = [p[1] for p in image]

    for x in range(min(xs) - 1, max(xs) + 2):
        for y in range(min(ys) - 1, max(ys) + 2):
            yield (x, y)

def num(a, b, image, dv):
    r =  "".join(image.get((a + x, b + y), dv) for (x, y) in
                 ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0),
                  (0, 1), (1, -1), (1, 0), (1, 1)))
    return int(r, 2)

def expand(image, algo, n=2):
    dv = '0'
    for i in range(n):
        new = dict()
        for p in points(image):
            new[p] = algo[num(*p, image, dv)]
        image = new
        dv = algo[int(dv * 9, 2)]
    return image

if __name__ == "__main__":
    with open('sample') as f:
        sample = f.read().strip()
    image, algo = parse(sample)
    new = expand(image, algo)
    p1 = list(new.values()).count('1')
    print("sample", p1)

    with open('input') as f:
        data = f.read().strip()
    image, algo = parse(data)
    p1 = list(expand(image, algo).values()).count('1')
    p2 = list(expand(image, algo, 50).values()).count('1')
    print("input", p1, p2)
