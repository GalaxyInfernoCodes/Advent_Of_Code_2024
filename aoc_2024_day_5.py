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


def fix_printing_order(
    sorting_instructions: dict[int, list[int]], printing_order: list[int]
) -> list[int]:
    for index in range(len(printing_order)):
        current_printing_entry = printing_order[index]
        if current_printing_entry in sorting_instructions:
            if index > 0:
                previous_printing_entries = printing_order[:index]
                wrongly_ordered_entries = set(previous_printing_entries).intersection(
                    set(sorting_instructions[current_printing_entry])
                )
                previous_printing_fixed = [
                    entry
                    for entry in previous_printing_entries
                    if entry not in wrongly_ordered_entries
                ]
                printing_order = (
                    previous_printing_fixed
                    + [current_printing_entry]
                    + [
                        entry
                        for entry in previous_printing_entries
                        if entry in wrongly_ordered_entries
                    ]
                    + printing_order[index + 1 :]
                )
                index -= len(wrongly_ordered_entries) + 1
    return printing_order


def return_middle_printing_entry(printing_order: list[int]) -> int:
    return printing_order[len(printing_order) // 2]


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=5, mode=mode)

    sorting_instructions = {}
    correct_printings_middle_entries = []

    for line in file_lines:
        if "|" in line:
            lower_number, upper_number = read_two_ints_from_string(line)
            if lower_number not in sorting_instructions:
                sorting_instructions[lower_number] = []
            sorting_instructions[lower_number].append(upper_number)
            # print("Sorting instructions:", sorting_instructions)
        elif "," in line:
            printing_order = [int(number) for number in line.split(",")]
            if check_printing_order(sorting_instructions, printing_order):
                correct_printings_middle_entries.append(
                    return_middle_printing_entry(printing_order)
                )
    return sum(correct_printings_middle_entries)


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=5, mode=mode)

    sorting_instructions = {}
    incorrect_printings_middle_entries = []

    for line in file_lines:
        if "|" in line:
            lower_number, upper_number = read_two_ints_from_string(line)
            if lower_number not in sorting_instructions:
                sorting_instructions[lower_number] = []
            sorting_instructions[lower_number].append(upper_number)
            # print("Sorting instructions:", sorting_instructions)
        elif "," in line:
            printing_order = [int(number) for number in line.split(",")]
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
