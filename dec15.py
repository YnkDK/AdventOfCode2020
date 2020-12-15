from collections import defaultdict


class RambunctiousRecitation:
    def __init__(self, seeds: str):
        self._memory = defaultdict(list)
        for i, seed in enumerate(seeds.split(',')):
            self._memory[int(seed)] = [i + 1]
            self._last_number_spoken = int(seed)

    def play(self, stop_turn: int):
        for turn in range(len(self._memory) + 1, stop_turn + 1):
            if len(self._memory[self._last_number_spoken]) == 1:
                self._last_number_spoken = 0
            else:
                last_spoken = self._memory[self._last_number_spoken][-1]
                before_then = self._memory[self._last_number_spoken][-2]
                self._last_number_spoken = last_spoken - before_then
            self._memory[self._last_number_spoken].append(turn)
            if len(self._memory[self._last_number_spoken]) == 3:
                self._memory[self._last_number_spoken].pop(0)

    @property
    def last_number_spoken(self):
        return self._last_number_spoken


def solve(seeds):
    rr = RambunctiousRecitation(seeds)
    rr.play(2020)
    yield rr.last_number_spoken

    rr = RambunctiousRecitation(seeds)
    rr.play(30000000)
    yield rr.last_number_spoken


if __name__ == '__main__':
    with open('dec15.input', 'r') as f:
        dec15 = f.read().strip()
    solutions = solve(dec15)

    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
