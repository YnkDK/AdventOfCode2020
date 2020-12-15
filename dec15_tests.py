"""Rambunctious Recitation (https://adventofcode.com/2020/day/15)
"""
import unittest

from dec15 import RambunctiousRecitation


class December15Test(unittest.TestCase):
    def test_parse(self):
        rr = RambunctiousRecitation('0,3,6')

        self.assertEqual(rr._memory[0], [1])
        self.assertEqual(rr._memory[3], [2])
        self.assertEqual(rr._memory[6], [3])

    def test_play(self):
        examples = [
            ('1,3,2', 1),
            ('2,1,3', 10),
            ('1,2,3', 27),
            ('2,3,1', 78),
            ('0,3,6', 436),
            ('3,2,1', 438),
            ('3,1,2', 1836)
        ]

        for seeds, expected_last_number_spoken in examples:
            with self.subTest():
                rr = RambunctiousRecitation(seeds)

                rr.play(2020)

                self.assertEqual(expected_last_number_spoken, rr.last_number_spoken)
