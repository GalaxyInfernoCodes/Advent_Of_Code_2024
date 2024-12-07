from aoc_utils import read_input_file, read_letter_grid_from_lines
import numpy as np
from tqdm import tqdm


def turn_right(direction: str) -> str:
    direction_map = {"^": ">", "v": "<", "<": "^", ">": "v"}
    return direction_map[direction]


def move_one_step(position: tuple[int, int], direction: str) -> tuple[int, int]:
    if direction == "^":
        new_position = (position[0] - 1, position[1])
    elif direction == "v":
        new_position = (position[0] + 1, position[1])
    elif direction == "<":
        new_position = (position[0], position[1] - 1)
    elif direction == ">":
        new_position = (position[0], position[1] + 1)
    return new_position


def check_if_position_still_on_grid(
    grid: np.ndarray, position: tuple[int, int]
) -> bool:
    return (
        position[0] >= 0
        and position[0] < grid.shape[0]
        and position[1] >= 0
        and position[1] < grid.shape[1]
    )


def move_until_obstacle_or_loop(
    grid: np.ndarray,
    position: tuple[int, int],
    direction: str,
    visited_positions: list[tuple[tuple[int, int], str]],
) -> tuple[tuple[int, int], str, list[tuple[tuple[int, int], str]]]:
    while check_if_position_still_on_grid(grid, position):
        # check if we looped (visited the same position with the same direction)
        if (position, direction) in visited_positions:
            return position, direction, visited_positions
        visited_positions.append((position, direction))

        grid[position[0], position[1]] = direction
        new_position = move_one_step(position, direction)

        if check_if_position_still_on_grid(grid, new_position) and grid[
            new_position
        ] in ["#", "O"]:
            break
        position = new_position
    new_direction = turn_right(direction)
    return position, new_direction, visited_positions


def find_start_position(grid: np.ndarray) -> tuple[tuple[int, int], str]:
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] in ["^", "v", "<", ">"]:
                return (i, j), grid[i, j]


# def count_visited_positions(grid: np.ndarray) -> int:
#     count = 0
#     for i in range(grid.shape[0]):
#         for j in range(grid.shape[1]):
#             if grid[i, j] in ["^", "v", "<", ">"]:
#                 count += 1
#     return count


def count_distinct_visited_positions(
    visited_positions: list[tuple[tuple[int, int], str]]
) -> int:
    # ignore directions and transform coordinates into set to get rid of duplicates
    distinct_positions = set(position for position, _ in visited_positions)
    return len(distinct_positions)


def create_obstacle_on_grid(grid: np.ndarray, position: tuple[int, int]) -> np.ndarray:
    new_grid = grid.copy()
    new_grid[position[0], position[1]] = "O"
    return new_grid


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=6, mode=mode)
    grid = read_letter_grid_from_lines(file_lines)

    position, direction = find_start_position(grid)
    visited_positions = []

    while check_if_position_still_on_grid(grid, position):
        position, direction, visited_positions = move_until_obstacle_or_loop(
            grid, position, direction, visited_positions
        )
    return count_distinct_visited_positions(visited_positions)


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=6, mode=mode)
    grid = read_letter_grid_from_lines(file_lines)

    start_position, start_direction = find_start_position(grid)

    loop_count = 0

    for i in tqdm(range(grid.shape[0]), desc="Rows"):
        for j in tqdm(range(grid.shape[1]), desc="Columns", leave=False):
            if grid[i, j] not in ["^", "v", "<", ">", "#"]:
                # print("obstacle at", (i, j))
                new_grid = create_obstacle_on_grid(grid, (i, j))
                position = start_position
                direction = start_direction
                visited_positions = []
                # print("new_grid", "obstacle at", (i, j))
                # print(new_grid)

                while check_if_position_still_on_grid(new_grid, position):
                    new_position, new_direction, visited_positions = (
                        move_until_obstacle_or_loop(
                            new_grid, position, direction, visited_positions
                        )
                    )
                    # if (i, j) == (2, 46):
                    #     print("new_position", new_position)
                    #     print("new_direction", new_direction)
                    if new_position == position and new_direction == direction:
                        loop_count += 1
                        break
                    position = new_position
                    direction = new_direction
    return loop_count


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
