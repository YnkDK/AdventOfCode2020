import collections


class Player:
    def __init__(self, initial_state, max_deck_size=None):
        if isinstance(initial_state, str):
            self.name, self._deck = Player._parse(initial_state)
        elif isinstance(initial_state, Player):
            self.name = initial_state.name
            self._deck = initial_state._deck.copy()
            while len(self._deck) > max_deck_size:
                self._deck.pop()

    @property
    def deck_count(self):
        return len(self._deck)

    def draw(self):
        try:
            return self._deck.popleft()
        except IndexError:
            return None

    def take_cards(self, winning_card, loosing_card):
        self._deck.append(winning_card)
        self._deck.append(loosing_card)

    def winning_score(self):
        score = 0
        multiplier = 1
        while len(self._deck) > 0:
            score += multiplier * self._deck.pop()
            multiplier += 1
        return score

    def new_deck(self, initial_state: str):
        self.name, self._deck = Player._parse(initial_state)

    def copy(self, max_deck_size):
        return Player(self, max_deck_size)

    def __str__(self):
        return f'{self.name}: {",".join(map(str, self._deck))}'

    @staticmethod
    def _parse(initial_state: str):
        state = initial_state.split('\n')
        return state[0][:-1], collections.deque(map(int, state[1:]))


class Combat:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2

    def play_round(self):
        card1 = self._player1.draw()
        if card1 is None:
            return self._player2.winning_score()

        card2 = self._player2.draw()
        if card2 is None:
            return self._player1.winning_score()

        if card1 > card2:
            self._player1.take_cards(card1, card2)
        else:
            self._player2.take_cards(card2, card1)


class RecursiveCombat:
    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        assert player1.name != player2.name

    @staticmethod
    def _play_recursively(player1: Player, player2: Player):
        previous_rounds = set()
        # If collecting cards by winning the round causes a player to have all of the cards, they win, and the game
        # ends.
        cards_count = player1.deck_count + player2.deck_count
        while player1.deck_count != cards_count and player2.deck_count != cards_count:
            # Before either player deals a card, if there was a previous round in this game that had exactly the same
            # cards in the same order in the same players' decks, the game instantly ends in a win for player 1.
            round_representation = str(player1) + str(player2)
            if round_representation in previous_rounds:
                return player1
            previous_rounds.add(round_representation)

            # Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing
            # the top card of their deck as normal.
            card1 = player1.draw()
            card2 = player2.draw()

            # If both players have at least as many cards remaining in their deck as the value of the card they just
            # drew, the winner of the round is determined by playing a new game of Recursive Combat
            if player1.deck_count >= card1 and player2.deck_count >= card2:
                # To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next
                # cards in their deck (the quantity of cards copied is equal to the number on the card they drew to
                # trigger the sub-game)
                winner_of_round = RecursiveCombat._play_recursively(player1.copy(card1), player2.copy(card2))
                # Note that the winner's card might be the lower-valued of the two cards if they won the round due to
                # winning a sub-game.
                if winner_of_round.name == player1.name:
                    player1.take_cards(card1, card2)
                else:
                    player2.take_cards(card2, card1)
            else:
                # Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of
                # the round is the player with the higher-value card.
                if card1 > card2:
                    player1.take_cards(card1, card2)
                else:
                    player2.take_cards(card2, card1)

        if player1.deck_count == cards_count:
            return player1
        return player2

    def play(self):
        return self._play_recursively(self._player1, self._player2)


def solve(p1_init_state: str, p2_init_state: str):
    player1 = Player(p1_init_state)
    player2 = Player(p2_init_state)
    game = Combat(player1, player2)
    winning_score = None

    while winning_score is None:
        winning_score = game.play_round()
    yield winning_score

    player1.new_deck(p1_init_state)
    player2.new_deck(p2_init_state)
    rc = RecursiveCombat(player1, player2)

    winner = rc.play()

    yield winner.winning_score()


if __name__ == '__main__':
    with open('dec22.input', 'r') as f:
        p1, p2 = f.read().split('\n\n')

    solutions = solve(p1, p2)
    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
