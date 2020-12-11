"""Seating System (https://adventofcode.com/2020/day/11)
"""
import unittest

from dec11 import solve, SeatingSystem, LINE_OF_SIGHT_MODE, OCCUPIED_SEAT, EMPTY_SEAT


class December11Test(unittest.TestCase):
    _EXAMPLE = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    def test_parse(self):
        s = SeatingSystem(December11Test._EXAMPLE)

        self.assertEqual(10, len(s._grid))
        for row in s._grid:
            self.assertTrue(all(c in ('.', 'L') for c in row))

    def test_first_round(self):
        s = SeatingSystem(December11Test._EXAMPLE)
        expected = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""
        did_change = next(s.rounds())

        self.assertTrue(did_change)
        self.assertEqual(expected, str(s))

    def test_second_round(self):
        s = SeatingSystem(December11Test._EXAMPLE)
        expected = """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##"""
        gen = s.rounds()
        next(gen)

        did_change = next(gen)

        self.assertTrue(did_change, str(s))
        self.assertEqual(expected, str(s))

    def test_example(self):
        s = SeatingSystem(December11Test._EXAMPLE)
        expected_end = """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##"""

        rounds = [did_change for did_change in s.rounds()]

        self.assertEqual(6, len(rounds))
        self.assertTrue(all(changed for changed in rounds[:-1]))
        self.assertFalse(rounds[-1])
        self.assertEqual(expected_end, str(s))
        self.assertEqual(37, s.number_of_seats_occupied)

    def test_no_line_of_sight(self):
        example = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""
        s = SeatingSystem(example, 5, LINE_OF_SIGHT_MODE)

        seats = [seat_state for seat_state in s._line_of_sight_seat_generator(3, 3)]

        self.assertEqual(0, len(seats))

    def test_all_lines_of_sight(self):
        example = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
        s = SeatingSystem(example, 5, LINE_OF_SIGHT_MODE)

        seats = [seat_state for seat_state in s._line_of_sight_seat_generator(4, 3)]

        self.assertEqual(8, len(seats))
        self.assertTrue(all(OCCUPIED_SEAT == state for state in seats))

    def test_one_empty_seat(self):
        example = """.............
.L.L.#.#.#.#.
............."""
        s = SeatingSystem(example, 5, LINE_OF_SIGHT_MODE)

        seats = [seat_state for seat_state in s._line_of_sight_seat_generator(1, 1)]

        self.assertEqual(1, len(seats))
        self.assertEqual(EMPTY_SEAT, seats[0])

    def test_solve(self):
        gen = solve(December11Test._EXAMPLE)

        results = [result for result in gen]

        self.assertEqual(2, len(results))
        self.assertEqual(37, results[0])
        self.assertEqual(26, results[1])
