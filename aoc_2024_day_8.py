from aoc_utils import (
    read_input_file,
    read_letter_grid_from_lines,
    check_if_position_still_on_grid,
)
import numpy as np
from math import gcd


def find_antenna_positions(
    antenna_grid: np.ndarray,
) -> dict[str, list[tuple[int, int]]]:
    antenna_positions = {}
    for i, row in enumerate(antenna_grid):
        for j, cell in enumerate(row):
            if cell != ".":
                if cell not in antenna_positions:
                    antenna_positions[cell] = []
                antenna_positions[cell].append((i, j))
    return antenna_positions


def calculate_antinode_positions_for_antenna_pair(
    antenna_1: tuple[int, int], antenna_2: tuple[int, int]
) -> list[tuple[int, int]]:
    difference = (antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1])
    first_antinode = (antenna_2[0] + difference[0], antenna_2[1] + difference[1])
    second_antinode = (antenna_1[0] - difference[0], antenna_1[1] - difference[1])
    return [first_antinode, second_antinode]


def calculate_antinode_positions_for_antenna_pair_part2(
    antenna_1: tuple[int, int], antenna_2: tuple[int, int], antenna_grid: np.ndarray
) -> list[tuple[int, int]]:
    difference = (antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1])
    # shorten distance by dividing by the greatest common divisor
    divisor = gcd(abs(difference[0]), abs(difference[1]))
    difference = (difference[0] // divisor, difference[1] // divisor)
    antinode_positions = [antenna_2, antenna_1]
    # one direction of antinodes (beyond antenna_2)
    possible_antinode_position = (
        antenna_2[0] + difference[0],
        antenna_2[1] + difference[1],
    )
    while check_if_position_still_on_grid(antenna_grid, possible_antinode_position):
        antinode_positions.append(possible_antinode_position)
        antenna_2 = possible_antinode_position
        possible_antinode_position = (
            antenna_2[0] + difference[0],
            antenna_2[1] + difference[1],
        )
    # other direction of antinodes (beyond antenna_1)
    possible_antinode_position = (
        antenna_1[0] - difference[0],
        antenna_1[1] - difference[1],
    )
    while check_if_position_still_on_grid(antenna_grid, possible_antinode_position):
        antinode_positions.append(possible_antinode_position)
        antenna_1 = possible_antinode_position
        possible_antinode_position = (
            antenna_1[0] - difference[0],
            antenna_1[1] - difference[1],
        )
    return antinode_positions


def calculate_antinode_grid(
    antenna_grid: np.ndarray,
    antenna_positions: dict[str, list[tuple[int, int]]],
    part2: bool = False,
) -> np.ndarray:
    antinode_grid = np.zeros(antenna_grid.shape)
    for _, positions in antenna_positions.items():
        antenna_pairs = (
            (pos1, pos2)
            for i, pos1 in enumerate(positions)
            for pos2 in positions[i + 1 :]
        )
        for antenna_1, antenna_2 in antenna_pairs:
            if part2:
                antinode_positions = (
                    calculate_antinode_positions_for_antenna_pair_part2(
                        antenna_1, antenna_2, antenna_grid
                    )
                )
            else:
                antinode_positions = calculate_antinode_positions_for_antenna_pair(
                    antenna_1, antenna_2
                )
            for antinode_position in antinode_positions:
                if check_if_position_still_on_grid(antinode_grid, antinode_position):
                    antinode_grid[antinode_position] = 1
    return antinode_grid


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=8, mode=mode)
    antenna_grid = read_letter_grid_from_lines(file_lines)
    antenna_positions = find_antenna_positions(antenna_grid)
    antinode_grid = calculate_antinode_grid(antenna_grid, antenna_positions)
    nr_of_antinodes = np.sum(antinode_grid)
    return nr_of_antinodes


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=8, mode=mode)
    antenna_grid = read_letter_grid_from_lines(file_lines)
    antenna_positions = find_antenna_positions(antenna_grid)
    antinode_grid = calculate_antinode_grid(antenna_grid, antenna_positions, part2=True)
    nr_of_antinodes = np.sum(antinode_grid)
    return nr_of_antinodes


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
