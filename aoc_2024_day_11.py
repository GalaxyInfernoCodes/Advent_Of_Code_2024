from aoc_utils import read_input_file


def blink_once(stone_list: list[int]) -> list[int]:
    index = 0
    while index < len(stone_list):
        stone = stone_list[index]
        if stone == 0:
            stone_list[index] = 1
            index += 1
        elif len(str(stone)) % 2 == 0:
            stone_one = int(str(stone)[: len(str(stone)) // 2])
            stone_two = int(str(stone)[len(str(stone)) // 2 :])
            stone_list = (
                stone_list[:index] + [stone_one, stone_two] + stone_list[index + 1 :]
            )
            index += 2
        else:
            stone_list[index] = stone * 2024
            index += 1
    return stone_list


def solve_part_1(mode: str = "example", blinks: int = 1):
    file_lines = read_input_file(day=11, mode=mode)
    initial_stones = [int(stone) for stone in file_lines[0].split()]

    stone_line = dict()
    for stone_value in initial_stones:
        if stone_value in stone_line:
            stone_line[stone_value] += 1
        else:
            stone_line[stone_value] = 1

    for _ in range(blinks):
        new_stone_line = dict()
        for stone_value, nr_of_stones in stone_line.items():
            new_stone_list = blink_once([stone_value])
            for new_stone in new_stone_list:
                if new_stone in new_stone_line:
                    new_stone_line[new_stone] += nr_of_stones
                else:
                    new_stone_line[new_stone] = nr_of_stones
        stone_line = new_stone_line

    stone_sum = sum(stone_line.values())

    return stone_sum


def main():
    print("Example part 1:", solve_part_1("example", 6))
    print("Example part 1:", solve_part_1("example", 25))
    print("Input part 1:", solve_part_1("input", 25))

    print("Example blinks 75:", solve_part_1("example", 75))
    print("Input blinks 75:", solve_part_1("input", 75))


if __name__ == "__main__":
    main()
