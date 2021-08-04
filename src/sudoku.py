import copy
from src.grid import Grid
from src.possibility import Possibility


class Sudoku:

    def __init__(self, sudoku_grid):
        self.sudoku_grid = sudoku_grid
        self.solutions_count = 0
        self.solutions = []

    def solve(self):
        """
        This method just calls the method solve_sodoku and prints all all solutions on the console.
        """
        self.solutions_count = 0
        self.solutions = []
        self.solve_sudoku(self.sudoku_grid)

        for index, solution in enumerate(self.solutions):
            print(f"Solution: {index + 1}")
            Grid.print_grid(solution)
        
        if len(self.solutions) == 0:
            print("No Solutions. Seems the puzzle is invalid!")

    def solve_sudoku(self, sudoku_grid):
        """
        This is the main method responsible for finding all possible solutions of a puzzle.
        It recursively keep searching for all the solutions.
        """
        result = Grid.check_grid(sudoku_grid)
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
                found_a_list = False
                found_a_single_possibility = False
                for i in range(0, 9):
                    for j in range(0, 9):
                        if (sudoku_grid[i][j] == 0 or
                                isinstance(sudoku_grid[i][j], list) is True):

                            sudoku_grid[i][j] = Possibility.all_possibilities(
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
            if Grid.check_grid(sudoku_grid) == "COMPLETE":
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
                # Grid.print_grid(sudoku_grid)
                i, j = all_list_indexes[0]
                for k in sudoku_grid[i][j]:
                    new_sudoku_grid = copy.deepcopy(sudoku_grid)
                    new_sudoku_grid[i][j] = k

                    if self.solve_sudoku(new_sudoku_grid) == "COMPLETE":
                        print("Complete")
