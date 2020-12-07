MY_BAG_COLOR = 'shiny gold'


class Rule:
    def __init__(self, color: str, count: int):
        self.color = color
        self.count = count
        self.is_visited = False

    def __repr__(self):
        return '({:s} - {:d})'.format(self.color, self.count)


class Regulations:
    def __init__(self, raw_input: str):
        self.rules = dict()

        for line in raw_input.split('\n'):
            substring = ' bags contain '
            index = line.find(substring)
            parent = line[:index]
            self.rules[parent] = []
            for child in line[index + len(substring):-1].split(','):
                count, color = child.strip().replace('bags', '').replace('bag', '').split(' ', 1)
                if count.isdigit():
                    self.rules[parent].append(Rule(color.strip(), int(count)))

    def outermost_bag_colors(self):
        outermost_bag_colors = set()
        for outermost_colors, children in self.rules.items():
            self._reset_is_visited()

            queue = list(children)
            for child in children:
                child.is_visited = True

            while queue:
                source = queue.pop()  # type: Rule
                if MY_BAG_COLOR == source.color:
                    outermost_bag_colors.add(outermost_colors)
                    break
                for rule in self.rules[source.color]:
                    if MY_BAG_COLOR == rule.color:
                        outermost_bag_colors.add(outermost_colors)
                        break
                    if not rule.is_visited:
                        queue.append(rule)
                        rule.is_visited = True
        self._reset_is_visited()
        return outermost_bag_colors

    def number_of_bags_to_buy(self, color: str = MY_BAG_COLOR):
        if len(self.rules[color]) == 0:
            return 1
        bag_count = 1
        for child in self.rules[color]:
            bag_count += child.count * self.number_of_bags_to_buy(child.color)
        return bag_count

    def _reset_is_visited(self):
        for key, values in self.rules.items():
            for value in values:
                value.is_visited = False


def solve(regulations: Regulations):
    bag_colors = regulations.outermost_bag_colors()
    yield len(bag_colors)
    # We already did buy the MY_BAG_COLOR bag, so subtract that one
    bags_to_buy = regulations.number_of_bags_to_buy() - 1
    yield bags_to_buy


if __name__ == '__main__':
    with open('dec07.input', 'r') as f:
        dec07_regulations = Regulations(f.read())
    solution_generator = solve(dec07_regulations)
    print('Part 1', next(solution_generator))
    print('Part 2', next(solution_generator))
