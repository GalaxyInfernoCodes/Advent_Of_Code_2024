from aoc_utils import read_input_file, read_two_ints_from_string
import re


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=3, part=1, mode=mode)

    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
    matches = []

    for line in file_lines:
        matches.extend(pattern.findall(line))

    multiplication_sum = 0
    for match in matches:
        left, right = read_two_ints_from_string(match)
        multiplication_sum += left * right

    return multiplication_sum


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=3, part=2, mode=mode)

    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
    matches = []

    for line in file_lines:
        matches.extend(pattern.findall(line))

    multiplication_sum = 0
    mul_active = True
    for match in matches:
        if match == "do()":
            mul_active = True
        elif match == "don't()":
            mul_active = False
        else:
            left, right = read_two_ints_from_string(match)
            if mul_active:
                multiplication_sum += left * right

    return multiplication_sum


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
