from aoc_utils import read_input_file


def convert_line_to_report(line: str) -> list[int]:
    line = line.strip()
    return [int(value) for value in line.split()]


def is_report_safe(report: list[int]) -> bool:
    diffs = [report[i] - report[i - 1] for i in range(1, len(report))]
    all_increasing = all(diff > 0 for diff in diffs)
    all_decreasing = all(diff < 0 for diff in diffs)

    if not (all_increasing or all_decreasing):
        return False

    all_distances_safe = all(abs(diff) >= 1 and abs(diff) <= 3 for diff in diffs)
    return all_distances_safe


def is_report_safe_v2(report: list[int]) -> bool:
    if is_report_safe(report):
        return True
    for i in range(0, len(report)):
        sub_report = report[:i] + report[i + 1 :]
        if is_report_safe(sub_report):
            return True
    return False


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=2, mode=mode)
    records = [convert_line_to_report(line) for line in file_lines]
    safe_records = [record for record in records if is_report_safe(record)]
    return len(safe_records)


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=2, mode=mode)
    records = [convert_line_to_report(line) for line in file_lines]
    safe_records = [record for record in records if is_report_safe_v2(record)]
    return len(safe_records)


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
