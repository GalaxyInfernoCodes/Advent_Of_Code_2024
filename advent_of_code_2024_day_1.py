from aoc_utils import read_input_file


def get_int_pair(double_int_str: str) -> tuple[int, int]:
    double_int_str = double_int_str.strip()
    left_str, right_str = double_int_str.split()

    first_int = int(left_str)
    last_int = int(right_str)
    return first_int, last_int


def build_lists(file_lines: list[str]) -> tuple[list[int], list[int]]:
    left_list = []
    right_list = []
    for line in file_lines:
        left_int, right_int = get_int_pair(line)
        left_list.append(left_int)
        right_list.append(right_int)
    return left_list, right_list


def solve_part_1(mode: str = "input"):
    file_lines = read_input_file(day=1, mode=mode)
    left_list, right_list = build_lists(file_lines)

    left_list.sort()
    right_list.sort()

    absolute_diff_list = [
        abs(left_int - right_int) for left_int, right_int in zip(left_list, right_list)
    ]
    return sum(absolute_diff_list)


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=1, mode=mode)
    left_list, right_list = build_lists(file_lines)

    similarity_scores = []
    for left_int in left_list:
        number_of_occurrences = right_list.count(left_int)
        similarity_scores.append(left_int * number_of_occurrences)

    return sum(similarity_scores)


def main():
    # Should be 11
    print("Example part 1:", solve_part_1("example"))
    # needs /inputs/input_day1.txt
    print("Input part 1:", solve_part_1("input"))

    # Should be 31
    print("Example part 2:", solve_part_2("example"))
    # needs /inputs/input_day1.txt
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
