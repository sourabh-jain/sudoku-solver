import sys
import json
from src.sudoku import Sudoku

PUZZLE_PATH = "puzzles"

if __name__ == "__main__":
    try:
        if len(sys.argv) <= 1:
            print("Please provide file name of the puzzle that you wish to solve!")
        else:
            puzzle_file = sys.argv[1]
            puzzle_file_path = f"{PUZZLE_PATH}/{puzzle_file}"

            with open(puzzle_file_path, "r") as file_reader:
                puzzle_content = json.loads(file_reader.read())

            Sudoku(puzzle_content).solve()
    except FileNotFoundError:
        print(
            f"The mentioned puzzle file does not exist at following path: {puzzle_file_path}")
