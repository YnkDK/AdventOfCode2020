"""Ticket Translation (https://adventofcode.com/2020/day/16)
"""
import itertools
import unittest

from dec16 import TicketTranslator

NOTES = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

PARSED_FIELDS = [
    ('class', 1, 3, 5, 7),
    ('row', 6, 11, 33, 44),
    ('seat', 13, 40, 45, 50)
]

YOUR_TICKET = (7, 1, 14)

NEARBY_TICKET = [
    (7, 3, 47),
    (40, 4, 50),
    (55, 2, 20),
    (38, 6, 12)
]

NOTES_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""


class December16Test(unittest.TestCase):
    def test_parse(self):
        tt = TicketTranslator(NOTES)

        for expected, actual in zip(PARSED_FIELDS, tt._fields):
            name, l1, h1, l2, h2 = expected
            self.assertEqual(name, actual.name)
            for i in itertools.chain(range(l1, h1 + 1), range(l2, h2 + 1)):
                self.assertTrue(actual.validator(i))
            self.assertFalse(actual.validator(l1 - 1))
            self.assertFalse(actual.validator(h1 + 1))
            self.assertFalse(actual.validator(l2 - 1))
            self.assertFalse(actual.validator(h2 + 1))

        self.assertEqual(YOUR_TICKET, tt._my_ticket)
        self.assertEqual(NEARBY_TICKET, tt._nearby_tickets)

    def test_remove_invalid_nearby_tickets(self):
        tt = TicketTranslator(NOTES)

        ticket_scanning_error_rate = tt.remove_invalid_nearby_tickets()

        self.assertEqual(71, ticket_scanning_error_rate)
        self.assertEqual(1, len(tt._nearby_tickets))
        self.assertEqual((7, 3, 47), tt._nearby_tickets[0])

    def test_remove_invalid_nearby_tickets_twice(self):
        tt = TicketTranslator(NOTES)

        tt.remove_invalid_nearby_tickets()
        ticket_scanning_error_rate = tt.remove_invalid_nearby_tickets()

        self.assertEqual(0, ticket_scanning_error_rate)

    def test_translate(self):
        expected = {'class': 12, 'row': 11, 'seat': 13}
        tt = TicketTranslator(NOTES_2)

        tt.translate()

        self.assertEqual(3, len(tt.my_ticket))
        for field, value in tt.my_ticket.items():
            self.assertIn(field.name, expected)
            self.assertEqual(expected[field.name], value)
