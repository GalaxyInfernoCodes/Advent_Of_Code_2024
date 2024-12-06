from aoc_utils import read_input_file, read_two_ints_from_string


def check_printing_order(
    sorting_instructions: dict[int, list[int]], printing_order: list[int]
) -> bool:
    for index, printing_entry in enumerate(printing_order):
        if printing_entry in sorting_instructions:
            if index > 0:
                previous_printing_entries = printing_order[:index]
                wrongly_ordered_entries = set(previous_printing_entries).intersection(
                    set(sorting_instructions[printing_entry])
                )
                if len(wrongly_ordered_entries) > 0:
                    return False
    return True


def reorder_entries(
    previous_entries: list[int],
    current_entry: int,
    wrongly_ordered_entries: set[int],
    remaining_entries: list[int],
) -> tuple[list[int], int]:
    correct_entries = [
        entry for entry in previous_entries if entry not in wrongly_ordered_entries
    ]
    reordered_entries = [
        entry for entry in previous_entries if entry in wrongly_ordered_entries
    ]
    new_order = (
        correct_entries + [current_entry] + reordered_entries + remaining_entries
    )
    new_index = len(correct_entries) - 1
    return new_order, new_index


def fix_printing_order(
    sorting_instructions: dict[int, list[int]], printing_order: list[int]
) -> list[int]:
    index = 0
    while index < len(printing_order):
        current_entry = printing_order[index]
        if current_entry in sorting_instructions and index > 0:
            previous_entries = printing_order[:index]
            required_entries = set(sorting_instructions[current_entry])
            wrongly_ordered_entries = set(previous_entries).intersection(
                required_entries
            )

            if wrongly_ordered_entries:
                printing_order, index = reorder_entries(
                    previous_entries,
                    current_entry,
                    wrongly_ordered_entries,
                    printing_order[index + 1 :],
                )
        index += 1
    return printing_order


def return_middle_printing_entry(printing_order: list[int]) -> int:
    return printing_order[len(printing_order) // 2]


def read_sorting_instructions(file_lines: list[str]) -> dict[int, list[int]]:
    sorting_instructions = {}
    for line in file_lines:
        if "|" in line:
            lower_number, upper_number = read_two_ints_from_string(line)
            if lower_number not in sorting_instructions:
                sorting_instructions[lower_number] = []
            sorting_instructions[lower_number].append(upper_number)
    return sorting_instructions


def read_printing_runs(file_lines: list[str]) -> list[list[int]]:
    printing_runs = []
    for line in file_lines:
        if "," in line:
            printing_order = [int(number) for number in line.split(",")]
            printing_runs.append(printing_order)
    return printing_runs


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=5, mode=mode)

    sorting_instructions = read_sorting_instructions(file_lines)
    printing_runs = read_printing_runs(file_lines)

    correct_printings_middle_entries = []
    for printing_order in printing_runs:
        if check_printing_order(sorting_instructions, printing_order):
            correct_printings_middle_entries.append(
                return_middle_printing_entry(printing_order)
            )
    return sum(correct_printings_middle_entries)


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=5, mode=mode)

    sorting_instructions = read_sorting_instructions(file_lines)
    printing_runs = read_printing_runs(file_lines)

    incorrect_printings_middle_entries = []
    for printing_order in printing_runs:
        if not check_printing_order(sorting_instructions, printing_order):
            fixed_printing_order = fix_printing_order(
                sorting_instructions, printing_order
            )
            incorrect_printings_middle_entries.append(
                return_middle_printing_entry(fixed_printing_order)
            )
    return sum(incorrect_printings_middle_entries)


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
