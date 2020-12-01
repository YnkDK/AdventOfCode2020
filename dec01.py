import itertools
import math
import typing


def solve(expense_report: typing.Tuple[int, ...], num_entries) -> int:
    for entries in itertools.combinations(expense_report, num_entries):
        if sum(entries) == 2020:
            return math.prod(entries)
    raise Exception('Nothing matched')


if __name__ == '__main__':
    with open('dec01.input', 'r') as f:
        my_expense = tuple(map(int, f.readlines()))
    result = solve(my_expense, 2)
    print(result)
    result = solve(my_expense, 3)
    print(result)
