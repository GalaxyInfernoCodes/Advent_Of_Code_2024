from aoc_utils import read_input_file, read_int_list_from_string
from itertools import product


def get_all_operator_combinations(
    nr_of_operators: int, part2: bool = False
) -> list[tuple[str, ...]]:
    if part2:
        return list(product(["add", "multiply", "concatenate"], repeat=nr_of_operators))
    else:
        return list(product(["add", "multiply"], repeat=nr_of_operators - 1))


class Equation:
    def __init__(self, line: str):
        integer_list = read_int_list_from_string(line)
        self.target_number = integer_list[0]
        self.input_numbers = integer_list[1:]

    def __repr__(self):
        return f"Equation(target_number={self.target_number}, input_numbers={self.input_numbers})"

    def check_if_solvable(self, part2: bool = False):
        nr_of_operators = len(self.input_numbers) - 1
        operator_combinations = get_all_operator_combinations(
            nr_of_operators, part2=part2
        )

        for operator_combination in operator_combinations:
            if self.check_operator_combination(operator_combination):
                return True
        return False

    def check_operator_combination(self, operator_combination: tuple[str, ...]):
        total = self.input_numbers[0]
        for i, operator in enumerate(operator_combination):
            if operator == "add":
                total += self.input_numbers[i + 1]
            elif operator == "multiply":
                total *= self.input_numbers[i + 1]
            elif operator == "concatenate":
                total = int(str(total) + str(self.input_numbers[i + 1]))
        return total == self.target_number


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=7, mode=mode)
    total_calibration_result = 0
    for line in file_lines:
        equation = Equation(line)
        if equation.check_if_solvable():
            total_calibration_result += equation.target_number
    return total_calibration_result


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=7, mode=mode)
    total_calibration_result = 0
    for line in file_lines:
        equation = Equation(line)
        if equation.check_if_solvable(part2=True):
            total_calibration_result += equation.target_number
    return total_calibration_result


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
