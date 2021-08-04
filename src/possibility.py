class Possibility:
    @staticmethod
    def all_possibilities(sudoku_grid, row_index, col_index):
        """
        This method takes sudoku_grid and a row_index and col_index and tries to compute
        all possible values that can come at that particular location. It checks
        horizontally, vertically and block wise. After that it returns the result
        in the form of list. If there is possibility of only one number, it returns
        the number else returns the entire possibility list.
        """

        h_possibilities = Possibility.horizontal_possibilities(sudoku_grid, row_index, [
            1, 2, 3, 4, 5, 6, 7, 8, 9])

        v_possibilities = Possibility.vertical_possibilities(
            sudoku_grid, col_index, h_possibilities)

        b_possibilities = Possibility.block_possibilities(
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

