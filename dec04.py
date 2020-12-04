import re
import typing


class Passport(dict):
    _REQUIRED_FIELDS = frozenset({'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'})
    _HCL_RE = re.compile(r'^#([0-9a-f]{6})$')
    _ECLS = frozenset({'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'})

    def __init__(self, passport_text: str):
        super().__init__()
        for field in passport_text.rstrip().split(' '):
            key, value = field.split(':')
            self[key] = value.strip()
        self.has_required_fields = Passport._REQUIRED_FIELDS.issubset(self.keys())

    def is_year_valid(self, key: str, minimum: int, maximum: int):
        try:
            assert len(self[key]) == 4
            assert minimum <= int(self[key]) <= maximum
        except (ValueError, AssertionError) as e:
            return False
        return True

    def is_height_valid(self):
        hgt = str(self['hgt'])
        unit = hgt[-2:]
        if unit not in ('cm', 'in'):
            return False
        height = int(hgt[:-2])
        if unit == 'cm':
            return 150 <= height <= 193
        if unit == 'in':
            return 59 <= height <= 76
        return True

    def is_hair_color_valid(self):
        return Passport._HCL_RE.match(self['hcl'])

    def is_eye_color_valid(self):
        return self['ecl'] in Passport._ECLS

    def is_pid_valid(self):
        return self['pid'].isnumeric() and len(self['pid']) == 9

    def is_valid(self):
        if not self.has_required_fields:
            return False
        try:
            assert self.is_year_valid('byr', 1920, 2002)
            assert self.is_year_valid('iyr', 2010, 2020)
            assert self.is_year_valid('eyr', 2020, 2030)
            assert self.is_height_valid()
            assert self.is_hair_color_valid()
            assert self.is_eye_color_valid()
            assert self.is_pid_valid()
        except AssertionError:
            return False
        return True


def parse_input(raw_input: str) -> typing.List[Passport]:
    passport = ""
    passports = []
    for line in raw_input.split('\n'):
        if line == '':
            passports.append(Passport(passport))
            passport = ""
            continue
        passport += line + " "
    else:
        passports.append(Passport(passport))
    return passports


def solve(passports: typing.List[Passport]):
    have_required_fields_count = 0
    valid_count = 0
    for passport in passports:
        have_required_fields_count += passport.has_required_fields
        valid_count += passport.is_valid()
    return have_required_fields_count, valid_count


if __name__ == '__main__':
    with open('dec04.input', 'r') as f:
        batch = parse_input(f.read())
    part1, part2 = solve(batch)
    print('Part 1', part1)
    print('Part 2', part2)
