def read_input_file(day: int, part: int = None, mode: str = "example"):
    if mode == "example":
        if part:
            file_path = f"inputs/example_day{day}_part{part}.txt"
        else:
            file_path = f"inputs/example_day{day}.txt"
    else:
        if part:
            file_path = f"inputs/input_day{day}_part{part}.txt"
        else:
            file_path = f"inputs/input_day{day}.txt"
    with open(file_path, "r") as f:
        lines = f.readlines()
    file_lines = [line.strip() for line in lines]
    return file_lines
