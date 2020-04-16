import numpy as np
import random
from chromosome import Chromosome

class initial_population():
    """ Klasa u kojoj se generise populacija- skup hromozoma"""

    def __init__(self):
        self.chromosomes = []
        return
    
    #Nc-broj kandidata
    def seed(self, Nc, known):
        self.chromosomes = []

        # Izracunaj koje vrednosti svako polje moze da sadrzi
        helper= Chromosome()
        helper.values = [[[] for j in range(0, 9)] for i in range(0, 9)]
        for row in range(0, 9):
            for column in range(0, 9):
                for value in range(1, 10):
                    if((known.values[row][column] == 0) and not
                            (known.is_column_duplicate(column, value) or known.is_block_duplicate(row, column,
                                                                                                   value) or known.is_row_duplicate(
                            row, value))):
                        # Polje je dostupno
                        helper.values[row][column].append(value)
                    elif (known.values[row][column] != 0):
                        # Date/poznate vrednosti
                        helper.values[row][column].append(known.values[row][column])
                        break

        for p in range(0, Nc):
            g = Chromosome()
            for i in range(0, 9):
                row = np.zeros(9).astype(int)
                for j in range(0, 9):

                    if (known.values[i][j] != 0):
                        row[j] = known.values[i][j]

                    elif (known.values[i][j] == 0):
                        row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]
                # Ako imamo duplikate, probaj ponovo
                while (len(list(set(row))) != 9):
                    for j in range(0, 9):
                        if (known.values[i][j] == 0):
                            row[j] = helper.values[i][j][random.randint(0, len(helper.values[i][j]) - 1)]

                g.values[i] = row

            self.chromosomes.append(g)
        self.update_fitness()

        print("Inicijalizacija populacije zavrsena")
        return

    def update_fitness(self):  # update fitnesa za svaki hromozom
        for chromosome in self.chromosomes:
            chromosome.update_fitness()
        return

    def sort(self):  # Sortiranje populacije u odnosu na fitnes
        for i in range(len(self.chromosomes) - 1):
            max = i
            for j in range(i + 1, len(self.chromosomes)):
                if self.chromosomes[max].fitness < self.chromosomes[j].fitness:
                    max = j
            temp = self.chromosomes[i]
            self.chromosomes[i] = self.chromosomes[max]
            self.chromosomes[max] = temp
        return

    def printBoard(self):
        for row in range(9):
            for col in range(9):
                print(self.chromosomes, end=' ')
                if col + 1 == 3 or col + 1 == 6:
                    print(" | ", end=' ')
            if row + 1 == 3 or row + 1 == 6:
                print("\n" + "-" * 25, end=' ')
            print()
        print()