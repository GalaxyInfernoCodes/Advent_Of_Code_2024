from aoc_utils import read_input_file, read_int_grid_from_lines
import numpy as np
from collections import deque


def get_neighbors(
    position: tuple[int, int], grid_shape: tuple[int, int]
) -> list[tuple[int, int]]:
    neighbors = []
    row, col = position
    max_row, max_col = grid_shape

    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < max_row - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < max_col - 1:
        neighbors.append((row, col + 1))  # Right

    return neighbors


def get_reachable_neighbors(
    topographic_map: np.ndarray, start_position: tuple[int, int]
) -> list[tuple[int, int]]:
    all_neighbors = get_neighbors(start_position, topographic_map.shape)
    start_height = topographic_map[start_position]
    return [
        neighbor
        for neighbor in all_neighbors
        if topographic_map[neighbor] == start_height + 1
    ]


def search_for_trailends(
    topographic_map: np.ndarray, start_position: tuple[int, int]
) -> int:
    visited = np.zeros_like(topographic_map, dtype=bool)
    visited[start_position] = True
    queue = deque([start_position])
    score = 0
    while queue:
        current_position = queue.pop()
        visited[current_position] = True
        current_value = topographic_map[current_position]
        if current_value == 9:
            score += 1
        for neighbor in get_reachable_neighbors(topographic_map, current_position):
            if not visited[neighbor] and neighbor not in queue:
                queue.append(neighbor)
    return score


def search_for_distinct_trails(
    topographic_map: np.ndarray, start_position: tuple[int, int]
) -> int:
    queue = deque([start_position])
    score = 0
    while queue:
        current_position = queue.pop()
        current_value = topographic_map[current_position]
        if current_value == 9:
            score += 1
        for neighbor in get_reachable_neighbors(topographic_map, current_position):
            queue.append(neighbor)
    return score


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=10, mode=mode)
    topographic_map = read_int_grid_from_lines(file_lines)

    sum_of_trailhead_scores = 0
    for row in range(topographic_map.shape[0]):
        for col in range(topographic_map.shape[1]):
            if topographic_map[row, col] == 0:
                trailhead_score = search_for_trailends(topographic_map, (row, col))
                sum_of_trailhead_scores += trailhead_score
    return sum_of_trailhead_scores


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=10, mode=mode)
    topographic_map = read_int_grid_from_lines(file_lines)

    sum_of_trailhead_scores = 0
    for row in range(topographic_map.shape[0]):
        for col in range(topographic_map.shape[1]):
            if topographic_map[row, col] == 0:
                trailhead_score = search_for_distinct_trails(
                    topographic_map, (row, col)
                )
                sum_of_trailhead_scores += trailhead_score
    return sum_of_trailhead_scores


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
