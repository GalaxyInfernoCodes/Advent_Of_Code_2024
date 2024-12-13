from aoc_utils import read_input_file, read_letter_grid_from_lines, add_tuples
import numpy as np
from collections import deque


def get_neighbor_plants(
    garden_grid: np.ndarray, region_grid: np.ndarray, position: tuple[int, int]
) -> np.ndarray:
    plant = garden_grid[position]
    found_neighbors = []
    for offset in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        neighbor_position = add_tuples(position, offset)
        if (
            0 <= neighbor_position[0] < garden_grid.shape[0]
            and 0 <= neighbor_position[1] < garden_grid.shape[1]
        ):
            if (
                garden_grid[neighbor_position] == plant
                and not region_grid[neighbor_position]
            ):
                region_grid[neighbor_position] = True
                found_neighbors.append(neighbor_position)
    return found_neighbors


def calculate_single_region(garden_grid: np.ndarray, position: tuple[int, int]) -> int:
    region_grid = np.zeros_like(garden_grid, dtype=bool)
    region_grid[position] = True
    neighbor_queue = deque(get_neighbor_plants(garden_grid, region_grid, position))
    while neighbor_queue:
        current_position = neighbor_queue.popleft()
        neighbor_queue.extend(
            get_neighbor_plants(garden_grid, region_grid, current_position)
        )
    return region_grid


def count_open_sides(region_grid: np.ndarray, position: tuple[int, int]) -> int:
    side_count = 0
    for offset in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        neighbor_position = add_tuples(position, offset)
        if (
            not (
                0 <= neighbor_position[0] < region_grid.shape[0]
                and 0 <= neighbor_position[1] < region_grid.shape[1]
            )
            or not region_grid[neighbor_position]
        ):
            side_count += 1
    return side_count


def count_connected_sides(region_grid: np.ndarray) -> int:
    print(f"Region grid:\n{region_grid}")
    side_count = 0
    # go through rows
    for i in range(region_grid.shape[0]):
        edges = []
        for j in range(region_grid.shape[1]):
            if region_grid[i, j] and (i == 0 or not region_grid[i - 1, j]):
                edges.append("-")
            else:
                edges.append(".")
        print(f"Row {i}: {''.join(edges).replace('.', ' ').split()}")
        nr_of_new_sides = len("".join(edges).replace(".", " ").split())
        side_count += nr_of_new_sides
    # check bottom of last row
    edges = []
    for j in range(region_grid.shape[1]):
        if region_grid[-1, j]:
            edges.append("-")
        else:
            edges.append(".")
    nr_of_new_sides = len("".join(edges).replace(".", " ").split())
    side_count += nr_of_new_sides
    print(f"Bottom row: {''.join(edges).replace('.', ' ').split()}")
    # check all columns
    for j in range(region_grid.shape[1]):
        edges = []
        for i in range(region_grid.shape[0]):
            if region_grid[i, j] and (j == 0 or not region_grid[i, j - 1]):
                edges.append("|")
            else:
                edges.append(".")
        nr_of_new_sides = len("".join(edges).replace(".", " ").split())
        side_count += nr_of_new_sides
        print(f"Column {j}: {''.join(edges).replace('.', ' ').split()}")
    # check right of last column
    edges = []
    for i in range(region_grid.shape[0]):
        if region_grid[i, -1]:
            edges.append("|")
        else:
            edges.append(".")
    nr_of_new_sides = len("".join(edges).replace(".", " ").split())
    side_count += nr_of_new_sides
    print(f"Right column: {''.join(edges).replace('.', ' ').split()}")
    return side_count


def calculate_fence_costs_part2(region_grid: np.ndarray) -> int:
    area = np.sum(region_grid)
    side_count = count_connected_sides(region_grid)
    print(f"Area: {area}, Side count: {side_count}")
    return area * side_count


def calculate_fence_costs(region_grid: np.ndarray) -> int:
    area = np.sum(region_grid)
    perimeter = 0
    for i, row in enumerate(region_grid):
        for j, cell in enumerate(row):
            if cell:
                edge_count = count_open_sides(region_grid, (i, j))
                perimeter += edge_count
    # print(f"Area: {area}, Perimeter: {perimeter}")
    return area * perimeter


def solve_part_1(mode: str = "example", part: str = None):
    file_lines = read_input_file(day=12, part=part, mode=mode)
    garden_grid = read_letter_grid_from_lines(file_lines)
    visited_grid = np.zeros_like(garden_grid)
    total_fence_costs = 0
    for i, row in enumerate(garden_grid):
        for j, plant in enumerate(row):
            if not visited_grid[i, j]:
                # print(f"Calculating fence costs for position {i, j}, plant {plant}")
                visited_grid[i, j] = True
                region_grid = calculate_single_region(garden_grid, (i, j))
                # print(f"Region grid:\n{region_grid}")
                fence_costs = calculate_fence_costs(region_grid)
                total_fence_costs += fence_costs
                visited_grid = np.logical_or(visited_grid, region_grid)
    return total_fence_costs


def solve_part_2(mode: str = "example", part: str = None):
    file_lines = read_input_file(day=12, part=part, mode=mode)
    garden_grid = read_letter_grid_from_lines(file_lines)
    visited_grid = np.zeros_like(garden_grid)
    total_fence_costs = 0
    for i, row in enumerate(garden_grid):
        for j, plant in enumerate(row):
            if not visited_grid[i, j]:
                print(f"Calculating fence costs for position {i, j}, plant {plant}")
                visited_grid[i, j] = True
                region_grid = calculate_single_region(garden_grid, (i, j))
                fence_costs = calculate_fence_costs_part2(region_grid)
                total_fence_costs += fence_costs
                visited_grid = np.logical_or(visited_grid, region_grid)
    return total_fence_costs


def main():
    print(
        "Example 1, part 1:",
        solve_part_1("example", part="1"),
    )
    print(
        "Example 2, part 1:",
        solve_part_1("example", part="2"),
    )
    print("Example 3, part 1:", solve_part_1("example", part="3"))
    print("Input part 1:", solve_part_1("input"))

    print("Example 1, part 2:", solve_part_2("example", part="1"))


if __name__ == "__main__":
    main()
