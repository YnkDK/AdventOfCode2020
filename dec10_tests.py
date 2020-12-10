"""Adapter Array (https://adventofcode.com/2020/day/10)
"""
import unittest

from dec10 import solve, AdapterList


class December10Test(unittest.TestCase):
    _EXAMPLE = """16
10
15
5
1
11
7
19
6
12
4"""

    def test_parse(self):
        al = AdapterList(map(int, December10Test._EXAMPLE.split()))

        sorted_by_jolts = sorted(al)

        self.assertEqual(16, al[0])
        self.assertEqual(4, al[-1])
        self.assertEqual(1, sorted_by_jolts[0])
        self.assertEqual(19, sorted_by_jolts[-1])

    def test_jolts_differences_count(self):
        al = AdapterList(map(int, December10Test._EXAMPLE.split()))

        counts = al.jolts_differences_count

        self.assertDictEqual({1: 7, 3: 5}, counts)

    def test_distinct_arrangement_count(self):
        al = AdapterList(map(int, December10Test._EXAMPLE.split()))

        distinct_arrangement_count = al.distinct_arrangement_count

        self.assertEqual(8, distinct_arrangement_count)

    def test_solve(self):
        al = AdapterList(map(int, December10Test._EXAMPLE.split()))

        solutions = [solution for solution in solve(al)]

        self.assertEqual(2, len(solutions))
        self.assertEqual(35, solutions[0])
        self.assertEqual(8, solutions[1])
