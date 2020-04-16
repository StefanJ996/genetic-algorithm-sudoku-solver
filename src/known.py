from chromosome import Chromosome


class Known(Chromosome):

    def __init__(self, values):
        self.values = values
        return
    # Proverava da li vec u nekom redu postoji element
    def is_row_duplicate(self, row, value):
        for column in range(0, 9):
            if (self.values[row][column] == value):
                return True
        return False

    # Proverava da li vec u nekoj koloni postoji element
    def is_column_duplicate(self, column, value):
        for row in range(0, 9):
            if (self.values[row][column] == value):
                return True
        return False
    # Proverava da li u bloku postoji element
    def is_block_duplicate(self, row, column, value):
        i = 3 * (row // 3)
        j = 3 * (column // 3)
        for m in range(i,i + 3):
            for n in range(j, j + 3):
                if self.values[m][n] == value:
                    return True
        return False