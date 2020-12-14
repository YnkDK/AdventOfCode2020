"""Shuttle Search (https://adventofcode.com/2020/day/13)
"""
import unittest

from dec13 import BusNotes


class December13Test(unittest.TestCase):
    _BUS_NOTES = BusNotes('7,13,x,x,59,x,31,19')

    def test_example(self):
        bus = self._BUS_NOTES.first_bus(939)

        self.assertEqual(59, bus.identifier)
        self.assertEqual(5, bus.wait_time)

    def test_equal(self):
        bus = self._BUS_NOTES.first_bus(7)

        self.assertEqual(7, bus.identifier)
        self.assertEqual(0, bus.wait_time)

    def test_shuttle_company_contest(self):
        timestamp = self._BUS_NOTES.shuttle_company_contest()

        self.assertEqual(1068781, timestamp)
