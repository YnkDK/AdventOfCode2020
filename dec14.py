from collections import namedtuple

MaskEntry = namedtuple('MaskEntry', ('index', 'value'))


class DockingSystem:
    _MASK_LINE_STARTS_WITH = 'mask = '
    _MEM_LINE_STARTS_WITH = 'mem['

    def __init__(self, version=1):
        self._mask = []
        self._mask_value = 0
        self._floating_mask = []
        self._memory = dict()

        if version == 1:
            self.__memory_updater = self._update_memory
        else:
            self.__memory_updater = self._update_memory_v2

    def execute_instruction(self, instruction: str):
        if instruction.startswith(DockingSystem._MASK_LINE_STARTS_WITH):
            mask = DockingSystem._parse_mask(instruction)
            self._update_mask(mask)
        elif instruction.startswith(DockingSystem._MEM_LINE_STARTS_WITH):
            index, value = DockingSystem._parse_memory(instruction)
            self.__memory_updater(index, value)
        else:
            raise NotImplemented(f'No instructions for {instruction}')

    def memory_sum(self):
        return sum(self._memory.values())

    def _update_mask(self, mask: str):
        self._mask = []
        self._mask_value = 0
        self._floating_mask = []
        for index, value in enumerate(mask):
            twos_complement_index = 35 - index
            try:
                value = int(value)
            except ValueError:
                assert value == 'X', f'Floating masks can only be marked as X, not "{value}"'
                self._floating_mask.append(twos_complement_index)
            else:
                self._mask_value |= value << twos_complement_index
                self._mask.append(MaskEntry(twos_complement_index, value))

    def _update_memory(self, index: int, value: int):
        for entry in self._mask:
            # https://stackoverflow.com/a/47990/4620080
            value ^= (-entry.value ^ value) & (1 << entry.index)
        self._memory[index] = value

    def _update_memory_v2(self, index: int, value: int):
        index |= self._mask_value
        for mask in range(2 ** len(self._floating_mask)):
            tmp = index
            for entry in self._floating_mask:
                if mask & 1:
                    tmp |= 1 << entry
                else:
                    tmp &= 0xFFFFFFFFF - 2 ** entry
                mask >>= 1
            self._memory[tmp] = value

    @staticmethod
    def _parse_mask(instruction: str):
        return instruction[len(DockingSystem._MASK_LINE_STARTS_WITH):]

    @staticmethod
    def _parse_memory(instruction: str):
        index, value = instruction.split(' = ')
        return int(index[len(DockingSystem._MEM_LINE_STARTS_WITH):-1]), int(value)


def solve(instructions: list):
    ds = DockingSystem()
    for instruction in instructions:
        ds.execute_instruction(instruction)
    yield ds.memory_sum()

    ds = DockingSystem(version=2)
    for instruction in instructions:
        ds.execute_instruction(instruction)
    yield ds.memory_sum()


if __name__ == '__main__':
    with open('dec14.input', 'r') as f:
        dec14 = f.read().split('\n')

    solutions = solve(dec14)
    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
