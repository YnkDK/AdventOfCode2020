class BootCode:
    def __init__(self, program: str):
        self.code = []
        for line in program.split('\n'):
            op, arg = line.split(' ')
            self.code.append((op, int(arg)))

    @staticmethod
    def execute(code):
        accumulator = 0
        visited = [False] * len(code)
        i = 0
        while i < len(visited) and not visited[i]:
            op, arg = code[i]
            visited[i] = True
            if op == 'acc' or op == 'nop':
                i += 1
                if op == 'acc':
                    accumulator += arg
            elif op == 'jmp':
                i += arg
        return accumulator, i

    def debug_infinite_loop(self):
        accumulator, _ = self.execute(self.code)
        return accumulator

    def hotfix_boot_code(self):
        for i, op_arg in enumerate(self.code):
            op, arg = op_arg
            if op == 'nop' or op == 'jmp':
                code = list(self.code)
                new_op = 'jmp' if op == 'nop' else 'nop'
                code[i] = (new_op, arg)
                accumulator, last_index = self.execute(code)
                if last_index == len(code):
                    return accumulator


def solve(boot_code: BootCode):
    yield boot_code.debug_infinite_loop()
    yield boot_code.hotfix_boot_code()


if __name__ == '__main__':
    with open('dec08.input', 'r') as f:
        dec08 = BootCode(f.read())
    solution_generator = solve(dec08)

    print('Part 1:', next(solution_generator))
    print('Part 2:', next(solution_generator))
