class BootCode:
    def __init__(self, program: str):
        self.code = []
        for line in program.split('\n'):
            op, arg = line.split(' ')
            self.code.append((op, int(arg)))

    def execute(self):
        accumulator = 0
        visited = [False] * len(self.code)
        i = 0
        while i < len(visited) and not visited[i]:
            op, arg = self.code[i]
            visited[i] = True
            if op == 'acc' or op == 'nop':
                i += 1
                if op == 'acc':
                    accumulator += arg
            elif op == 'jmp':
                i += arg
        return accumulator, i == len(self.code)

    def debug_infinite_loop(self):
        accumulator, _ = self.execute()
        return accumulator

    def hotfix_boot_code(self):
        for i, (op, arg) in enumerate(self.code):
            if op in ('nop', 'jmp'):
                new_op = 'jmp' if op == 'nop' else 'nop'
                self.code[i] = (new_op, arg)
                accumulator, was_exit_success = self.execute()
                self.code[i] = (op, arg)
                if was_exit_success:
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
