#!/usr/bin/env python3
import re
import sys

pp_keys = {"byr": None,
           "iyr": None,
           "eyr": None,
           "hgt": None,
           "hcl": None,
           "ecl": None,
           "pid": None,
           "cid": "North Pole"}

required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}



    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.


def verify1(pp):
    keys = set(pp.keys())
    if not required_keys.issubset(keys):
        return False
    return True

def verify2(pp):
    if not (re.match(r'^[\d]{4}$', pp['byr']) and
            int(pp['byr']) in range(1920, 2003)):
        return False
    if not (re.match(r'^[\d]{4}$', pp['iyr']) and
            int(pp['iyr']) in range(2010, 2021)):
        return False
    if not (re.match(r'^[\d]{4}$', pp['eyr']) and
            int(pp['eyr']) in range(2020, 2031)):
        return False

    mob = re.match(r'^([\d]+)(cm|in)$', pp['hgt'])
    if (mob):
        val = mob.group(1)
        if mob.group(2) == 'in':
            if not int(val) in range(59, 77):
                return False
        else:
            if not int(val) in range(150, 194):
                return False

    if not (re.match(r'^#[0-9a-f]{6}$', pp['hcl'])):
        return False
    if not pp['ecl'] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    if not (re.match(r'^[\d]{9}$', pp['pid'])):
        return False
    return True

def parse(fname):
    c1 = 0
    c2 = 0
    with open(fname) as f:
        data = f.read()
        passports = data.split("\n\n")
        for i, p in enumerate(passports):
            p = p.replace('\n', ' ')
            pairs = list(map(lambda x: x.split(':'), p.split()))
            pp = dict(pairs)
            if verify1(pp):
                c1 += 1
                if verify2(pp):
                    c2 += 1
                    print(p)
    return c1, c2

if __name__ == "__main__":
    fname = sys.argv[1]
    print(parse(fname))
