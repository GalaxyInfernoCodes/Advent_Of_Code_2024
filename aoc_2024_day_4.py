from aoc_utils import (
    read_input_file,
    read_letter_grid_from_lines,
    extract_rows_from_grid,
    extract_columns_from_grid,
    extract_diagonals_from_grid,
)
import numpy as np


def extract_A_blocks_from_grid(grid: np.ndarray) -> list[np.ndarray]:
    blocks = []
    for i, j in np.ndindex(grid.shape):
        if (
            grid[i, j] == "A"
            and i + 1 < grid.shape[0]
            and i - 1 >= 0
            and j + 1 < grid.shape[1]
            and j - 1 >= 0
        ):
            blocks.append(grid[i - 1 : i + 2, j - 1 : j + 2])
    return blocks


def check_block_for_XMAS(block: np.ndarray) -> bool:
    if set([block[0, 0], block[2, 2]]) == set(["M", "S"]) and set(
        [block[0, 2], block[2, 0]]
    ) == set(["M", "S"]):
        return True
    return False


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=4, mode=mode)
    letter_grid = read_letter_grid_from_lines(file_lines)

    rows = extract_rows_from_grid(letter_grid)
    columns = extract_columns_from_grid(letter_grid)
    diagonals = extract_diagonals_from_grid(letter_grid)

    target_substring = "XMAS"
    total_count = 0

    for line in rows + columns + diagonals:
        total_count += line.count(target_substring)

    return total_count


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=4, mode=mode)
    letter_grid = read_letter_grid_from_lines(file_lines)

    a_blocks = extract_A_blocks_from_grid(letter_grid)
    total_count = 0
    for block in a_blocks:
        if check_block_for_XMAS(block):
            total_count += 1
    return total_count


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
