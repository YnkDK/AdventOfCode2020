"""Rain Risk (https://adventofcode.com/2020/day/12)
"""
import unittest

from dec12 import Ferry


class December12Test(unittest.TestCase):
    def test_example(self):
        example = ['F10', 'N3', 'F7', 'R90', 'F11']
        f = Ferry()

        for instruction in example:
            f.move(instruction)

        self.assertEqual(25, f.manhattan_distance_moved)
