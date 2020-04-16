import numpy as np
import copy
class Brute():
    def __init__(self):
        self.values = np.zeros((9,9)).astype(int)
        return
    def readInput(self, filename):
        input = open(filename, "r")
        self.values = np.loadtxt(input).reshape((9, 9)).astype(int)
        return
    def solve(self):
        try:
            self.fillAllObvious()
        except:
            return False
        if self.isComplete():
            self.printBoard()
            return True
        i,j = 0,0
        for m in range(9):
            for n in range(9):
                if self.values[m][n] == 0:
                    i,j = m,n
        possibilities = self.getPossibilities(i,j)
        for value in possibilities:
            snapshot = copy.deepcopy(self.values)
            self.values[i][j] = value
            result = self.solve()
            if result == True:
                return True
            else:
                self.values = copy.deepcopy(snapshot)

        return False

    def fillAllObvious(self):
        while True:
            somethingChanged = False
            for i in range(0, 9):
                for j in range(0, 9):
                    possibilities = self.getPossibilities(i, j)
                    if possibilities == False:
                        continue
                    if len(possibilities) == 0:
                        raise RuntimeError("Nema vise mogucnosti")
                    if len(possibilities) == 1:
                        self.values[i][j] = possibilities[0]
                        somethingChanged = True
            if somethingChanged == False:
                return

    def getPossibilities(self,i,j):
        if (self.values[i][j] != 0):
            return False

        possibilities = [i for i in range(1,10)]
        for val in self.values[i]:
            if val in possibilities:
                possibilities.remove(val)

        for idx in range(0,9):
            if self.values[idx][j] in possibilities:
                possibilities.remove(self.values[idx][j])
        iStart = (i // 3) * 3
        jStart = (j // 3) * 3
        for m in range(iStart,iStart + 3):
            for n in range(jStart, jStart + 3):
                if self.values[m][n] in possibilities:
                    possibilities.remove(self.values[m][n])

        return list(possibilities)

    def printBoard(self):

        for row in range(9):
            for col in range(9):
                print(self.values[row][col], end=' ')
                if col + 1 == 3 or col + 1 == 6:
                    print(" | ", end=' ')
            if row + 1 == 3 or row + 1 == 6:
                print("\n" + "-" * 25, end=' ')
            print()
        print()
    def isComplete(self):
        for row in self.values:
            for col in row:
                if (col == 0):
                    return False
        return True
