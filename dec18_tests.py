"""Operation Order (https://adventofcode.com/2020/day/18)
"""
import unittest

from dec18 import ChildMath

EXAMPLES = (
    '1 + (2 * 3) + (4 * (5 + 6))',
    '2 * 3 + (4 * 5)',
    '5 + (8 * 3 + 9 + 3 * 4 * 3)',
    '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
    '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
)


class December18Test(unittest.TestCase):
    def test_no_parenthesis(self):
        ch = ChildMath()

        solution = ch.solve('1 + 2 * 3 + 4 * 5 + 6')

        self.assertEqual(71, solution)

    def test_parenthesis(self):
        expected = (51, 26, 437, 12240, 13632)
        cm = ChildMath()

        for expression, expected_result in zip(EXAMPLES, expected):
            with self.subTest():
                solution = cm.solve(expression)
                self.assertEqual(expected_result, solution)

    def test_advanced_no_parenthesis(self):
        ch = ChildMath()
        ch.switch_to_advanced_math()

        solution = ch.solve('1 + 2 * 3 + 4 * 5 + 6')

        self.assertEqual(231, solution)

    def test_advanced(self):
        expected = (51, 46, 1445, 669060, 23340)
        cm = ChildMath()
        cm.switch_to_advanced_math()

        for expression, expected_result in zip(EXAMPLES, expected):
            with self.subTest():
                result = cm.solve(expression)
                self.assertEqual(expected_result, result)
