class Grid:

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
    def check_grid(sudoku_grid):
        """
        This method checks if the specified sudoku_grid is valid, invalid or complete.
        """

        # Horizontal check
        for i in range(0, 9):
            if Grid.unique_list(sudoku_grid[i]) is False:
                return "INVALID"

        flag_no_left = True

        # Vertical check
        for j in range(0, 9):
            lst = []
            for i in range(0, 9):
                lst.append(sudoku_grid[i][j])
                if sudoku_grid[i][j] == 0 or isinstance(sudoku_grid[i][j], list):
                    flag_no_left = False

            if Grid.unique_list(lst) is False:
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

                if Grid.unique_list(lst) is False:
                    return "INVALID"

        # Check the count of 0, if there are no 0 that means it is COMPLETE
        if flag_no_left:
            return "COMPLETE"
        else:
            return "VALID"
