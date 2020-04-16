import numpy as np
import random

class Chromosome():
    """ Predstavlja jedan hromozom, odnosno jedno resenje, dat kao matrica, inicijalno je prazna. Ocena prilagodjenosti se inicijalno postavlja na 0-prazna polja"""

    def __init__(self):
        self.values = np.zeros((9, 9)).astype(int)
        self.fitness = 0
        return

        """ Funkcija fitness odredjuje koliko je kandidat blizu da bude zapravo resenje. Znamo, da svaka kolona, red i blok u igri sudoku sadrzi brojeve [1,9] bez ponavljanja. Sto ima vise ponavljanja(duplikata) fitness vrednost je manja. """
    def update_fitness(self):
        columnCount = np.zeros(9).astype(int)
        blockCount = np.zeros(9).astype(int)
        rowCount = np.zeros(9).astype(int)
        columnSum = 0
        blockSum = 0
        rowSum = 0

        for i in range(9):
            nonzero = 0
            for j in range(9):
                columnCount[self.values[j][i] - 1] += 1
            for k in range(9):
                if columnCount[k] != 0:
                    nonzero += 1
            nonzero = nonzero / 9
            columnSum = (columnSum + nonzero)
            columnCount = np.zeros((9)).astype(int)
        columnSum = columnSum / 9

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                blockCount[self.values[i][j] - 1] += 1
                blockCount[self.values[i][j + 1] - 1] += 1
                blockCount[self.values[i][j + 2] - 1] += 1

                blockCount[self.values[i + 1][j] - 1] += 1
                blockCount[self.values[i + 1][j + 1] - 1] += 1
                blockCount[self.values[i + 1][j + 2] - 1] += 1

                blockCount[self.values[i + 2][j] - 1] += 1
                blockCount[self.values[i + 2][j + 1] - 1] += 1
                blockCount[self.values[i + 2][j + 2] - 1] += 1

                nonzero = 0
                for k in range(0, 9):
                    if blockCount[k] != 0:
                        nonzero += 1
                nonzero = nonzero / 9
                blockSum = blockSum + nonzero
                blockCount = np.zeros((9)).astype(int)
        blockSum = blockSum / 9
        
        for i in range(9):
            nonzero = 0
            for j in range(9):
                rowCount[self.values[i][j] - 1] += 1
            for k in range(9):
                if rowCount[k] != 0:
                    nonzero += 1
            nonzero = nonzero / 9
            rowSum = (rowSum + nonzero)
            rowCount = np.zeros((9)).astype(int)
        rowSum = rowSum / 9
        
        if (int(columnSum) == 1 and int(blockSum) == 1 and int(rowSum) == 1):
            fitness = 1.0
        else:
            fitness = columnSum * blockSum * rowSum

        self.fitness = fitness
        return
    def mutate(self, mutation_rate, known):

        #Vrsi se mutacija nad hromozomima sa verovatnocom mutation_rate.

        r = random.random()        #bira nasumicno broj iz intervala (0,1)
        success = False             #inicijalno, postavljamo success na False
        if (r < mutation_rate):  # dolazi do mutacije ako je r<mutation_rate
            while (not success):
                # random biramo red u kojem ce se obaviti zamena kolona 
                row1 = random.randint(0, 8)

                # potom, random biramo 2 kolone
                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while (from_column == to_column):
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)

                    # Proveri da li su polja prazna
                if (known.values[row1][from_column] == 0 and known.values[row1][to_column] == 0):
                    # proveri da nema duplikata u redovima,kolonama,blokovima
                    if (not known.is_column_duplicate(to_column, self.values[row1][from_column])
                            and not known.is_column_duplicate(from_column, self.values[row1][to_column])
                            and not known.is_block_duplicate(row1, to_column, self.values[row1][from_column])
                            and not known.is_block_duplicate(row1, from_column, self.values[row1][to_column])):
                        # Zameni vrednosti
                        tmp = self.values[row1][to_column]
                        self.values[row1][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = tmp
                        success = True

        return success