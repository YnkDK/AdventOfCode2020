"""Conway Cubes (https://adventofcode.com/2020/day/17)
"""
import unittest

from dec17 import ConwayCubes

EXAMPLE = '.#.\n..#\n###'


class December17Test(unittest.TestCase):
    def test_parse(self):
        cc = ConwayCubes(EXAMPLE)

        self.assertEqual(5, cc.active_count)
        self.assertTrue(cc.is_active((0, 1, 0)))
        self.assertTrue(cc.is_active((1, 2, 0)))
        self.assertTrue(cc.is_active((2, 0, 0)))
        self.assertTrue(cc.is_active((2, 1, 0)))
        self.assertTrue(cc.is_active((2, 2, 0)))
        self.assertFalse(cc.is_active((0, 0, 0)))
        self.assertFalse(cc.is_active((0, 2, 0)))
        self.assertFalse(cc.is_active((1, 0, 0)))
        self.assertFalse(cc.is_active((1, 1, 0)))

    def test_one_cycle(self):
        cc = ConwayCubes(EXAMPLE)

        cc.run_cycle()

        self.assertEqual(11, len(cc._state))
        self.assertEqual(11, cc.active_count)
        # | . . . .
        # | # . . .
        # | . . # .
        # | . # . .
        self.assertTrue(cc.is_active((1, 0, -1)))
        self.assertTrue(cc.is_active((2, 2, -1)))
        self.assertTrue(cc.is_active((3, 1, -1)))
        # | . . .
        # | # . #
        # | . # #
        # | . # .
        self.assertTrue(cc.is_active((2, 2, 0)))
        self.assertTrue(cc.is_active((3, 1, 0)))
        self.assertTrue(cc.is_active((2, 1, 0)))
        self.assertTrue(cc.is_active((1, 2, 0)))
        self.assertTrue(cc.is_active((1, 0, 0)))
        # | . . .
        # | # . .
        # | . . #
        # | . # .
        self.assertTrue(cc.is_active((3, 1, 1)))
        self.assertTrue(cc.is_active((1, 0, 1)))
        self.assertTrue(cc.is_active((2, 2, 1)))
