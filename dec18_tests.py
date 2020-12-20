"""Operation Order (https://adventofcode.com/2020/day/18)
"""
import unittest

from dec18 import ChildMath


class December18Test(unittest.TestCase):
    def test_no_parenthesis(self):
        ch = ChildMath()

        solution = ch.solve('1 + 2 * 3 + 4 * 5 + 6')

        self.assertEqual(71, solution)

    def test_parenthesis(self):
        cm = ChildMath()

        solution = cm.solve('1 + (2 * 3) + (4 * (5 + 6))')

        self.assertEqual(51, solution)
