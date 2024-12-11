from aoc_utils import read_input_file
from tqdm import tqdm


class FilesystemEntry:
    def __init__(self, value: int, length: int):
        self.value = value
        self.length = length

    def __repr__(self):
        return f"Value: {self.value}, Length: {self.length}\n"


class Filesystem:
    def __init__(self, puzzle_input: str):
        self.filesystem_entries = dict()
        self.puzzle_input = puzzle_input

    def __repr__(self):
        return "".join(
            (
                str(entry.value) * entry.length
                if entry.value is not None
                else "." * entry.length
            )
            for entry in self.filesystem_entries.values()
        )

    def expand_into_block_entries(self):
        file_id = 0
        # switch empty space and file id via flipping a boolean
        empty_space = False
        expanded_index = 0
        for block_length_str in self.puzzle_input:
            block_length = int(block_length_str)
            if empty_space:
                self.filesystem_entries[expanded_index] = FilesystemEntry(
                    value=None, length=block_length
                )
            else:
                self.filesystem_entries[expanded_index] = FilesystemEntry(
                    value=file_id, length=block_length
                )
                file_id += 1
            empty_space = not empty_space
            expanded_index += block_length

    def expand_into_single_entries(self):
        file_id = 0
        # switch empty space and file id via flipping a boolean
        empty_space = False
        expanded_index = 0
        for block_length_str in self.puzzle_input:
            block_length = int(block_length_str)
            for start_index in range(expanded_index, expanded_index + block_length):
                if empty_space:
                    self.filesystem_entries[start_index] = FilesystemEntry(
                        value=None, length=1
                    )
                else:
                    self.filesystem_entries[start_index] = FilesystemEntry(
                        value=file_id, length=1
                    )
                expanded_index += 1
            if not empty_space:
                file_id += 1
            empty_space = not empty_space

    def find_first_fitting_space_entry(self, file_length: int, before_index: int):
        for start_index, space_entry in self.filesystem_entries.items():
            if (
                space_entry.value is None
                and space_entry.length >= file_length
                and start_index < before_index
            ):
                return start_index
        return None

    # part 1
    def compact_filesystem_part1(self):
        file_entries = [
            (file_index, file_entry)
            for file_index, file_entry in self.filesystem_entries.items()
            if file_entry.value is not None
        ]
        for _ in tqdm(range(len(file_entries)), desc="compacting filesystem part 1"):
            filler_file_index, filler_file_entry = file_entries.pop()
            # find target space if it exists
            target_space_start_index = self.find_first_fitting_space_entry(
                filler_file_entry.length, filler_file_index
            )
            if target_space_start_index is not None:
                if target_space_start_index >= filler_file_index:
                    return
                switch_two_filesystem_entries(
                    self.filesystem_entries,
                    filler_file_index,
                    target_space_start_index,
                )

    def compact_filesystem_part2(self):
        file_entries = [
            (file_index, file_entry)
            for file_index, file_entry in self.filesystem_entries.items()
            if file_entry.value is not None
        ]
        for _ in tqdm(range(len(file_entries)), desc="compacting filesystem part 2"):
            filler_file_index, filler_file_entry = file_entries.pop()
            # find target space if it exists
            target_space_start_index = self.find_first_fitting_space_entry(
                filler_file_entry.length, filler_file_index
            )
            if target_space_start_index is not None:
                if target_space_start_index >= filler_file_index:
                    return
                if (
                    self.filesystem_entries[target_space_start_index].length
                    == filler_file_entry.length
                ):
                    switch_two_filesystem_entries(
                        self.filesystem_entries,
                        filler_file_index,
                        target_space_start_index,
                    )
                else:
                    insert_file_into_partial_space_block(
                        self.filesystem_entries,
                        target_space_start_index,
                        filler_file_entry.value,
                        filler_file_entry.length,
                    )
                    self.filesystem_entries[filler_file_index] = FilesystemEntry(
                        value=None, length=filler_file_entry.length
                    )
                self.filesystem_entries = dict(sorted(self.filesystem_entries.items()))

    def flatten_filesystem_entries(self):
        separate_entries = [
            [file_entry.value] * file_entry.length
            for file_entry in self.filesystem_entries.values()
        ]
        separate_entries = [item for sublist in separate_entries for item in sublist]
        return separate_entries

    def calculate_filesystem_checksum(self):
        separate_entries = self.flatten_filesystem_entries()
        checksum = 0
        for index, entry_value in enumerate(separate_entries):
            if entry_value is not None:
                checksum += index * entry_value
        return checksum


def switch_two_filesystem_entries(
    filesystem_entries: dict[int, FilesystemEntry],
    start_index_1: int,
    start_index_2: int,
):
    entry_1 = filesystem_entries[start_index_1]
    entry_2 = filesystem_entries[start_index_2]
    filesystem_entries[start_index_1] = entry_2
    filesystem_entries[start_index_2] = entry_1


def insert_file_into_partial_space_block(
    filesystem_entries: dict[int, FilesystemEntry],
    start_index: int,
    file_id: int,
    file_length: int,
):
    # Check if the file can fit into the space
    if filesystem_entries[start_index].length < file_length:
        raise ValueError("File length exceeds available space.")

    # Calculate remaining space after inserting the file
    remaining_space_length = filesystem_entries[start_index].length - file_length

    # Insert the file into the start of the space block
    filesystem_entries[start_index] = FilesystemEntry(value=file_id, length=file_length)

    # Adjust the space block to fit the file, if there is remaining space
    if remaining_space_length > 0:
        filesystem_entries[start_index + file_length] = FilesystemEntry(
            value=None, length=remaining_space_length
        )


def solve_part_1(mode: str = "example"):
    file_lines = read_input_file(day=9, mode=mode)
    diskmap = file_lines[0]
    filesystem = Filesystem(diskmap)
    filesystem.expand_into_single_entries()
    filesystem.compact_filesystem_part1()
    return filesystem.calculate_filesystem_checksum()


def solve_part_2(mode: str = "example"):
    file_lines = read_input_file(day=9, mode=mode)
    diskmap = file_lines[0]
    filesystem = Filesystem(diskmap)
    filesystem.expand_into_block_entries()
    filesystem.compact_filesystem_part2()
    return filesystem.calculate_filesystem_checksum()


def main():
    print("Example part 1:", solve_part_1("example"))
    print("Input part 1:", solve_part_1("input"))

    print("Example part 2:", solve_part_2("example"))
    print("Input part 2:", solve_part_2("input"))


if __name__ == "__main__":
    main()
