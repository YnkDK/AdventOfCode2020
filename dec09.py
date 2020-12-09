class ExchangeMaskingAdditionSystem:
    def __init__(self, numbers: str, preamble_length: int = 25):
        self.numbers = list(map(int, numbers.split('\n')))
        self.preamble_length = preamble_length

    def _gen_first_second(self, i):
        for j in range(i - self.preamble_length, i):
            first = self.numbers[j]
            for k in range(j + 1, i):
                second = self.numbers[k]
                yield first, second

    def find_first_error(self):
        for i in range(self.preamble_length, len(self.numbers)):
            to_check = self.numbers[i]
            for first, second in self._gen_first_second(i):
                if first + second == to_check:
                    break
            else:
                return to_check, i

    def break_encryption(self, error_index: int):
        to_match = self.numbers[error_index]
        for i in range(0, error_index):
            contiguous_sum = self.numbers[i]
            smallest = self.numbers[i]
            largest = self.numbers[i]
            for j in range(i + 1, error_index):
                jth_number = self.numbers[j]
                if jth_number < smallest:
                    smallest = jth_number
                if jth_number > largest:
                    largest = jth_number

                contiguous_sum += jth_number
                if contiguous_sum > to_match:
                    break
                elif contiguous_sum == to_match:
                    return smallest + largest


def solve(xmas: ExchangeMaskingAdditionSystem):
    first_error, error_index = xmas.find_first_error()
    yield first_error
    yield xmas.break_encryption(error_index)


if __name__ == '__main__':
    with open('dec09.input', 'r') as f:
        dec09 = ExchangeMaskingAdditionSystem(f.read())
    solution_generator = solve(dec09)

    part1 = next(solution_generator)
    part2 = next(solution_generator)

    assert part1 == 1492208709
    assert part2 == 238243506

    print('Part 1', part1)
    print('Part 2', part2)
