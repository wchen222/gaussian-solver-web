import numpy as np


class GaussianElimination:
    def __init__(self, matrix):
        self.m = matrix
        self.pivot_vals = []

    def check_pivot(self, row):
        if self.m[row][row]:
            return True
        return False

    # operations
    def swap(self, row1, row2):
        self.m[[row1, row2]] = self.m[[row2, row1]]

    def add(self, acceptor, adder, count):  # we add adder to acceptor count times
        self.m[acceptor] -= count * self.m[adder]  # if positive it will subtract
        self.m += 0  # to avoid -0

    def mul(self, row, val):
        mul = 1 / val
        self.m[row] *= mul

    def setup(self):
        column_one = self.m[:, 0]
        if 1 in column_one:
            piv_inx = np.where(column_one == 1)[0][0]
            self.swap(0, piv_inx)

    # to work on
    def set_pivot(self, row):  # if there are 2 column we want c to go up to 1
        original_row = row
        column_count = self.m.shape[1]
        current_column = row  # we initially start with column = row, then column = row + 1
        pivot_val = self.m[row][row]  # get the next pivot
        if pivot_val == 0:  # move bottom then right
            while current_column < column_count:  # while we are in bounds
                column = self.m[row+1:, current_column]
                non_zero_inx = np.nonzero(column)
                if non_zero_inx[0].size > 0:  # there contains a pivot below
                    pivot_val = self.m[row][current_column]
                    self.mul(row, pivot_val)
                    self.pivot_vals.append([row, current_column])
                    return row, current_column
                else:
                    # moving to next row
                    row += 1
                    if row >= self.m.shape[0]:
                        current_column += 1
                        row = original_row
            return row, row
        else:
            # default val is a pivot
            self.mul(row, pivot_val)
            self.pivot_vals.append([row, row])
            return row, row

    # forms

    def ref(self, m):
        row = m.shape[0]
        col = m.shape[1]
        self.setup()
        for i in range(row):
            if i >= col:
                return i
            cords = self.set_pivot(i)
            self.clear_under(cords)

    def rref(self, m):
        self.ref(m)

        # rref
        for i in reversed(self.pivot_vals):
            self.clear_over(i)

    def clear_under(self, pivot_cord):  # keep going down and clearing under
        row = pivot_cord[0]
        col = pivot_cord[1]
        current_row = row + 1
        column = self.m[current_row:, col]
        for val in column:
            self.add(current_row, row, val)
            current_row += 1

    def clear_over(self, pivot_num):  # keep going up and clearing above
        row = pivot_num[0]
        col = pivot_num[1]
        current_row = row - 1
        column = self.m[0:current_row + 1, col]
        column = column[::-1]
        for val in column:
            self.add(current_row, row, val)
            current_row -= 1

    def solve(self, m):
        print(f"Original matrix:\n{m}")
        self.rref(m)
        print(f"RREF form:\n{m + 0}")


def parse_matrix(matrix_str):
    lines = matrix_str.split("\n")
    arr = []
    for i in lines:
        arr.append(i.split())
    matrix = np.array(arr).astype(float)
    return matrix


def display(matrix_str):
    m = parse_matrix(matrix_str)
    solver = GaussianElimination(m)
    solver.solve(m)
    
    return m
