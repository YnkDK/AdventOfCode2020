from collections import defaultdict


class AdapterList(list):
    def __init__(self, seq=()):
        super().__init__(seq)
        self._jolts_differences_count = None
        self._distinct_arrangement_count = None

    def warm_up_cache(self):
        # Joined up the two first solutions into one loop
        self._jolts_differences_count = {1: 0, 3: 1}
        sorted_by_jolts = [0] + sorted(self)
        sorted_by_jolts.append(sorted_by_jolts[-1] + 3)

        destination = sorted_by_jolts.pop()
        backtrack_count = defaultdict(int)
        backtrack_count[destination] = 1

        i = len(sorted_by_jolts) - 1
        for jolt in reversed(sorted_by_jolts):
            if i > 0:
                previous_jolt = sorted_by_jolts[i - 1]
                self._jolts_differences_count[jolt - previous_jolt] += 1
            backtrack_count[jolt] = backtrack_count[jolt + 1] + backtrack_count[jolt + 2] + backtrack_count[jolt + 3]
            i -= 1
        self._distinct_arrangement_count = backtrack_count[0]

    @property
    def jolts_differences_count(self) -> dict:
        if self._jolts_differences_count is None:
            differences_count = {1: 0, 3: 1}
            sorted_by_jolts = sorted(self)
            for index, adapter_jolts in enumerate(sorted_by_jolts):
                previous_jolt = sorted_by_jolts[index - 1] if index > 0 else 0
                differences_count[adapter_jolts - previous_jolt] += 1
            self._jolts_differences_count = differences_count
        return self._jolts_differences_count

    @property
    def distinct_arrangement_count(self) -> int:
        if self._distinct_arrangement_count is None:
            sorted_by_jolts = [0] + sorted(self)
            sorted_by_jolts.append(sorted_by_jolts[-1] + 3)
            backtrack_count = defaultdict(int)

            destination = sorted_by_jolts.pop()
            backtrack_count[destination] = 1

            for i in reversed(sorted_by_jolts):
                backtrack_count[i] = backtrack_count[i + 1] + backtrack_count[i + 2] + backtrack_count[i + 3]
            self._distinct_arrangement_count = backtrack_count[0]
        return self._distinct_arrangement_count


def solve(adapter_list: AdapterList):
    adapter_list.warm_up_cache()
    jolts_differences_count = adapter_list.jolts_differences_count
    yield jolts_differences_count[1] * jolts_differences_count[3]
    yield adapter_list.distinct_arrangement_count


if __name__ == '__main__':
    with open('dec10.input', 'r') as f:
        dec10 = AdapterList(map(int, f.read().split()))
    solutions_generator = solve(dec10)

    part1 = next(solutions_generator)
    part2 = next(solutions_generator)

    print('Part 1:', part1)
    print('Part 2:', part2)

    assert part1 == 2030
    assert part2 == 42313823813632
