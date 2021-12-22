#!/usr/bin/env python

from collections import defaultdict

sample = (4,8)
real = (3,10)

class Dice:
    i = 0
    def roll(self):
        self.i += 1
        return self.i

def play(p1, p2, lim=1000):
    p1score = 0
    p2score = 0
    dice = Dice()
    while True:
        p1 = (p1 + sum(dice.roll() for _ in range(3))) % 10
        p1score += p1 or 10
        if p1score >= 1000:
            break
        p2 = (p2 + sum(dice.roll() for _ in range(3))) % 10
        p2score += p2 or 10
        if p2score >= 1000:
            break
    rolls = dice.i
    lscore = min(p1score, p2score)
    res = rolls * lscore
    return res

dfreq = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

def dwins(players, i=0, cnt=1, seq=None, lim=21):
    cpos, cscore = players[i]
    for r, rf in dfreq.items():
        npos = (cpos + r) % 10
        nscore = cscore + (npos or 10)
        nseq = (seq or tuple()) + (r,)
        ncnt = cnt * rf
        if nscore >= 21:
            yield (i, ncnt, nseq)
        else:
            nplayers = list(players)
            nplayers[i] = (npos, nscore)
            yield from dwins(nplayers, (i + 1) % 2, ncnt, nseq)

def dplay(p1, p2):
    score = [0, 0]
    for g in dwins([(p1, 0), (p2, 0)]):
        score[g[0]]+=g[1]
    return max(score)

if __name__ == "__main__":
    print(play(*sample))
    print(play(*real))
    print(dplay(*real))
