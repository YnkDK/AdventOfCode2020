"""Crab Combat (https://adventofcode.com/2020/day/22)
"""
import unittest

from dec22 import Player, Combat, RecursiveCombat

p1 = 'Player 1:\n9\n2\n6\n3\n1'
p2 = 'Player 2:\n5\n8\n4\n7\n10'


class December22Test(unittest.TestCase):
    def test_first_round(self):
        player1 = Player(p1)
        player2 = Player(p2)
        game = Combat(player1, player2)

        game.play_round()

        self.assertListEqual([2, 6, 3, 1, 9, 5], list(player1._deck))
        self.assertListEqual([8, 4, 7, 10], list(player2._deck))

    def test_all(self):
        winning_score = None
        player1 = Player(p1)
        player2 = Player(p2)
        game = Combat(player1, player2)
        rounds_played = 0

        while winning_score is None:
            winning_score = game.play_round()
            rounds_played += 1

        self.assertEqual(30, rounds_played)
        self.assertEqual(306, winning_score)

    def test_copy_player(self):
        player = Player(p1)

        player_copy = player.copy(player.deck_count)
        player.winning_score()

        self.assertNotEqual(id(player), id(player_copy))
        self.assertNotEqual(id(player._deck), id(player_copy._deck))
        self.assertEqual(0, player.deck_count)
        self.assertEqual(5, player_copy.deck_count)

    def test_recursive_combat(self):
        player1 = Player(p1)
        player2 = Player(p2)
        rc = RecursiveCombat(player1, player2)

        result = rc.play()

        self.assertEqual(player2, result)
