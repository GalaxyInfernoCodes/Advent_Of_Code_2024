import re


def read_input_file(day: int, part: int = None, mode: str = "example"):
    if mode == "example":
        if part:
            file_path = f"inputs/example_day{day}_part{part}.txt"
        else:
            file_path = f"inputs/example_day{day}.txt"
    else:
        file_path = f"inputs/input_day{day}.txt"
    with open(file_path, "r") as f:
        lines = f.readlines()
    file_lines = [line.strip() for line in lines]
    return file_lines


def read_two_ints_from_string(line: str) -> tuple[int, int]:
    numbers = re.findall(r"-?\d+", line)
    if len(numbers) < 2:
        raise ValueError("The input line does not contain two integers.")
    return int(numbers[0]), int(numbers[1])
