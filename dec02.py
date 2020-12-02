import re
import typing


class Password:
    _parser = re.compile(r'(\d+)-(\d+) (\w): (\w+)')

    def __init__(self, policy_and_password: str):
        groups = self._parser.match(policy_and_password).groups()
        self.min = int(groups[0])
        self.max = int(groups[1])
        self.character = groups[2]
        self.password = groups[3]

    def is_valid_occurrences(self) -> bool:
        return self.min <= self.password.count(self.character) <= self.max

    def is_valid_positions(self) -> bool:
        is_first_match = self.password[self.min - 1] == self.character
        is_second_match = self.password[self.max - 1] == self.character
        return is_first_match ^ is_second_match


def solve(passwords: typing.List[Password]):
    number_valid_occurrences = 0
    number_valid_positions = 0
    for password in passwords:
        number_valid_occurrences += password.is_valid_occurrences()
        number_valid_positions += password.is_valid_positions()
    return number_valid_occurrences, number_valid_positions


if __name__ == '__main__':
    with open('dec02.input', 'r') as f:
        dec02_passwords = list(map(Password, f.readlines()))
    print(solve(dec02_passwords))
