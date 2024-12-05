import re
import numpy as np


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


def read_letter_grid_from_lines(lines: list[str]) -> np.ndarray:
    char_lines = [list(line.strip()) for line in lines]
    return np.array(char_lines)


def extract_rows_from_grid(grid: np.ndarray) -> list[str]:
    rows = ["".join(row) for row in grid]
    reversed_rows = [row[::-1] for row in rows]
    return rows + reversed_rows


def extract_columns_from_grid(grid: np.ndarray) -> list[str]:
    columns = ["".join(column) for column in grid.T]
    reversed_columns = [column[::-1] for column in columns]
    return columns + reversed_columns


def extract_diagonals_from_grid(grid: np.ndarray) -> list[str]:
    grid_height, grid_width = grid.shape
    diagonals = []
    for k in range(grid_width):
        diagonals.append("".join(np.diag(grid, k)))
    for k in range(1, grid_height):
        diagonals.append("".join(np.diag(grid, -k)))

    flipped_array = np.fliplr(grid)
    flipped_height, flipped_width = flipped_array.shape
    for k in range(flipped_width):
        diagonals.append("".join(np.diag(flipped_array, k)))
    for k in range(1, flipped_height):
        diagonals.append("".join(np.diag(flipped_array, -k)))
    reversed_diagonals = [diagonal[::-1] for diagonal in diagonals]
    return diagonals + reversed_diagonals
