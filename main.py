import copy
import json
import sys

PUZZLE_PATH = "puzzles"


class Sudoku:

    def __init__(self, sudoku_grid):
        self.sudoku_grid = sudoku_grid
        self.solutions_count = 0
        self.solutions = []

    @staticmethod
    def print_grid(sudoku_grid):
        """
        This method takes a sudoku grid and prints on the console.
        It can also print if the grid has possibility list.
        """
        for i in range(0, 9):

            single_row = []
            for j in range(0, 9):
                element = sudoku_grid[i][j]

                if isinstance(sudoku_grid[i][j], list):
                    single_row.append(" " * (9-len(element)))
                    single_row.append(
                        "".join(map(lambda x: str(x), element)))
                else:
                    single_row.append(" " * 8)
                    single_row.append(str(element))

            single_row_str = " ".join(single_row) + "\n"

            print(single_row_str)

    @staticmethod
    def unique_list(lst):
        """
        This method checks if the specified list is unique or not.
        It will ignore any 0 or possibility list from the comparison.

        """
        new_list = []
        for e in lst:
            if e != 0 and isinstance(e, list) is False:
                new_list.append(e)

        return len(set(new_list)) == len(new_list)

    @staticmethod
    def check_grid(sudoku_grid):
        """
        This method checks if the specified sudoku_grid is valid, invalid or complete.
        """

        # Horizontal check
        for i in range(0, 9):
            if Sudoku.unique_list(sudoku_grid[i]) is False:
                return "INVALID"

        flag_no_left = True

        # Vertical check
        for j in range(0, 9):
            lst = []
            for i in range(0, 9):
                lst.append(sudoku_grid[i][j])
                if sudoku_grid[i][j] == 0 or isinstance(sudoku_grid[i][j], list):
                    flag_no_left = False

            if Sudoku.unique_list(lst) is False:
                return "INVALID"

        # Block check
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                lst = []
                lst.append(sudoku_grid[i][j])
                lst.append(sudoku_grid[i+1][j])
                lst.append(sudoku_grid[i+2][j])
                lst.append(sudoku_grid[i][j+1])
                lst.append(sudoku_grid[i+1][j+1])
                lst.append(sudoku_grid[i+2][j+1])
                lst.append(sudoku_grid[i][j+2])
                lst.append(sudoku_grid[i+1][j+2])
                lst.append(sudoku_grid[i+2][j+2])

                if Sudoku.unique_list(lst) is False:
                    return "INVALID"

        # Check the count of 0, if there are no 0 that means it is COMPLETE
        if flag_no_left:
            return "COMPLETE"
        else:
            return "VALID"

    def solve(self):
        """
        This method just calls the method solve_sodoku and prints all all solutions on the console.
        """
        self.solutions_count = 0
        self.solutions = []
        self.solve_sudoku(self.sudoku_grid)

        for index, solution in enumerate(self.solutions):
            print(f"Solution: {index + 1}")
            self.print_grid(solution)

    def solve_sudoku(self, sudoku_grid):
        """
        This is the main method responsible for finding all possible solutions of a puzzle.
        It recursively keep searching for all the solutions.
        """
        result = self.check_grid(sudoku_grid)
        if result == "COMPLETE":
            self.solutions_count += 1
            self.solutions.append(copy.deepcopy(sudoku_grid))
            return result

        elif result == "INVALID":
            return result

        else:

            found_a_single_possibility = True

            """
            The first step to solve a sudoku is to first solve the cells which have only one
            possible value. This is because they save us from the hunt to find the correct
            value from a list of possible values. Also, solving them may open doors for
            finding more such cells which have only one possible value. This loop will
            keep going until there are no cells remaining with single possibility.
            """
            while found_a_single_possibility:
                all_list_indexes = []
                # Find the first cell with a zero
                found_a_list = False
                found_a_single_possibility = False
                for i in range(0, 9):
                    for j in range(0, 9):
                        if (sudoku_grid[i][j] == 0 or
                                isinstance(sudoku_grid[i][j], list) is True):

                            sudoku_grid[i][j] = self.all_possibilities(
                                sudoku_grid, i, j)
                            if sudoku_grid[i][j] == "INVALID":
                                return "INVALID"

                            elif isinstance(sudoku_grid[i][j], list):
                                found_a_list = True
                                all_list_indexes.append((i, j))
                            else:
                                found_a_single_possibility = True
                                break
                    if found_a_single_possibility:
                        break

            # Sometimes even the single possibility can lead us to the solution.
            # Check if we have reached to the solution.
            if self.check_grid(sudoku_grid) == "COMPLETE":
                self.solutions_count += 1
                self.solutions.append(copy.deepcopy(sudoku_grid))
                return result

            """
            Utill now we have exhausted all the single possbility cells and we
            are left with all possibility lists. Now simply take first such list
            possbility cell and assume this is a correct solution, recursively go
            ahead and find try to solve again. If this was wrong we would get INVALID
            at some point of time and we would get back here. Basically all the
            possibility list values of all such cells would be assumed in the hunt to
            find solutions. The good thing is, this would work well if we have multiple
            solutions as we do not stop after getting one solution.
            """
            if found_a_list:
                # self.print_grid(sudoku_grid)
                i, j = all_list_indexes[0]
                for k in sudoku_grid[i][j]:
                    new_sudoku_grid = copy.deepcopy(sudoku_grid)
                    new_sudoku_grid[i][j] = k

                    if self.solve_sudoku(new_sudoku_grid) == "COMPLETE":
                        print("Complete")

    @staticmethod
    def all_possibilities(sudoku_grid, row_index, col_index):
        """
        This method takes sudoku_grid and a row_index and col_index and tries to compute
        all possible values that can come at that particular location. It checks
        horizontally, vertically and block wise. After that it returns the result
        in the form of list. If there is possibility of only one number, it returns
        the number else returns the entire possibility list.
        """

        h_possibilities = Sudoku.horizontal_possibilities(sudoku_grid, row_index, [
            1, 2, 3, 4, 5, 6, 7, 8, 9])

        v_possibilities = Sudoku.vertical_possibilities(
            sudoku_grid, col_index, h_possibilities)

        b_possibilities = Sudoku.block_possibilities(
            sudoku_grid, row_index, col_index, v_possibilities)

        if len(b_possibilities) == 1:
            return b_possibilities[0]
        elif len(b_possibilities) == 0:
            return "INVALID"
        else:
            return b_possibilities

    @staticmethod
    def horizontal_possibilities(sudoku_grid, row_index, possible_values):
        """
        This method finds out all possible values for the specified row in the sudoku_grid.
        """
        for j in range(0, 9):
            if sudoku_grid[row_index][j] in possible_values:
                possible_values.remove(sudoku_grid[row_index][j])

        return possible_values

    @staticmethod
    def vertical_possibilities(sudoku_grid, col_index, possible_values):
        """
        This method finds out all possible values for the specified column in the sudoku_grid.
        """
        for i in range(0, 9):
            if sudoku_grid[i][col_index] in possible_values:
                possible_values.remove(sudoku_grid[i][col_index])

        return possible_values

    @staticmethod
    def block_possibilities(sudoku_grid, row_index, col_index, possible_values):
        """
        This method finds out all possible values for a particular block in the sudoku_grid
        There can be 9 blocks. Each block is a collection of 3x3 matrix.
        1 2 3
        4 5 6
        7 8 9
        First it finds the start row and start column index of the block based
        on row_index and col_index and then find the possibilities.
        """
        start_row = (row_index//3)*3
        start_col = (col_index//3)*3

        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if sudoku_grid[i][j] in possible_values:
                    possible_values.remove(sudoku_grid[i][j])
        return possible_values


if __name__ == "__main__":
    try:
        if len(sys.argv) < 1:
            print("Please provide file name of the puzzle that you wish to solve!")

        puzzle_file = sys.argv[1]
        puzzle_file_path = f"{PUZZLE_PATH}/{puzzle_file}"

        with open(puzzle_file_path, "r") as file_reader:
            puzzle_content = json.loads(file_reader.read())

        Sudoku(puzzle_content).solve()
    except FileNotFoundError:
        print(
            f"The mentioned puzzle file does not exist at following path: {puzzle_file_path}")
