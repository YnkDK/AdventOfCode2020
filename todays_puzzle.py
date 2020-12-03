import datetime

from aocd.models import Puzzle

year = datetime.datetime.now().year
day = datetime.datetime.now().day

puzzle = Puzzle(year=year, day=day)

with open('dec{:02d}.input'.format(day), 'w') as f:
    f.write(puzzle.input_data)

with open('dec{:02d}.py'.format(day), 'w') as f:
    f.write("""def solve():
    pass


if __name__ == '__main__':
    with open('dec{:02d}.input', 'r') as f:
        _ = list(map(int, f.readlines()))
""".format(day))

with open('dec{:02d}_tests.py'.format(day), 'w') as f:
    f.write("""\"\"\"{:s} ({:s})
\"\"\"
import unittest
from dec{:02d} import solve


class December{:02d}Test(unittest.TestCase):
    def test(self):
        pass
""".format(puzzle.title, puzzle.url, day, day))
