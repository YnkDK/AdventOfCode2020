"""Docking Data (https://adventofcode.com/2020/day/14)
"""
import unittest

from dec14 import DockingSystem


class December14Test(unittest.TestCase):
    def test_one_step(self):
        ds = DockingSystem()

        ds.execute_instruction('mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
        ds.execute_instruction('mem[8] = 11')

        self.assertEqual(73, ds._memory[8])
        self.assertEqual(73, ds.memory_sum())

    def test_v2_42_100(self):
        ds = DockingSystem(version=2)

        ds.execute_instruction('mask = 000000000000000000000000000000X1001X')
        ds.execute_instruction('mem[42] = 100')

        self.assertEqual(ds._memory[26], 100)
        self.assertEqual(ds._memory[27], 100)
        self.assertEqual(ds._memory[58], 100)
        self.assertEqual(ds._memory[59], 100)
        self.assertEqual(ds.memory_sum(), 400)

    def test_v2_26_1(self):
        ds = DockingSystem(version=2)

        ds.execute_instruction('mask = 00000000000000000000000000000000X0XX')
        ds.execute_instruction('mem[26] = 1')

        self.assertEqual(ds.memory_sum(), 8)
        self.assertEqual(ds._memory[16], 1)
        self.assertEqual(ds._memory[17], 1)
        self.assertEqual(ds._memory[18], 1)
        self.assertEqual(ds._memory[19], 1)
        self.assertEqual(ds._memory[24], 1)
        self.assertEqual(ds._memory[25], 1)
        self.assertEqual(ds._memory[26], 1)
        self.assertEqual(ds._memory[27], 1)
