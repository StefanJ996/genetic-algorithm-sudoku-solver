import numpy as np
import random
from chromosome import Chromosome



class CycleCrossover():
    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        """ Geni za novi hromozom se uzimaju od 2 roditelja, primenjujuci odgovarajuci tip ukrstanja """
        child1 = Chromosome()
        child2 = Chromosome()

        # pravimo kopiju roditeljskih gena koje cemo koristiti da ne bi uticale na original
        child1.values = np.copy(parent1.values)
        child2.values = np.copy(parent2.values)

        r = random.random()
        # Perform crossover.
        if (r < crossover_rate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most 8) rows.
            #biramo 2 tacke za crossover, koje moraju biti razlicite
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while (crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)

            if (crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp

            for i in range(crossover_point1, crossover_point2):
                child1.values[i], child2.values[i] = self.crossover_rows(child1.values[i], child2.values[i])
        return child1, child2

    #par1-hromozomi jednog roditelja, par2-hromozomi drugog roditelja
    #implementacija cycle crossover-a
    #na pocetku imamo nizove za decu koji su imaju prazna polja(ispunjeni 0)
    def crossover_rows(self, par1, par2):
        child_row1 = np.zeros(9).astype(int)
        child_row2 = np.zeros(9).astype(int)

        #lista polja koja se nisu koristila
        remaining = [i for i in range(1, 10)]
        cycle = 0

        while ((0 in child_row1) and (0 in child_row2)):  # Dok ne popuno decu u potpunosti
            if (cycle % 2 == 0):  # Parni ciklusi- vrednosti ciklusa iz roditelja1 idu u dete1. Analogno za roditelj2
                # Trazi prvu neobradjenu vrednost
                index = self.find_unused(par1, remaining)
                start = par1[index]
                remaining.remove(par1[index])
                child_row1[index] = par1[index]
                child_row2[index] = par2[index]
                next = par2[index]

                while (next != start):  # Dok se ne vratimo u pocetnu tacku, tj dok ne dodje do ciklusa
                    index = self.find_value(par1, next)
                    child_row1[index] = par1[index]
                    remaining.remove(par1[index])
                    child_row2[index] = par2[index]
                    next = par2[index]

                cycle += 1

            else:  # Neparni ciklusi-tu vrsimo zamenu, vrednosti ciklusa iz roditelja1 ide u dete2 i obrnuto
                index = self.find_unused(par1, remaining)
                start = par1[index]
                remaining.remove(par1[index])
                child_row1[index] = par2[index]
                child_row2[index] = par1[index]
                next = par2[index]

                while (next != start):
                    index = self.find_value(par1, next)
                    child_row1[index] = par2[index]
                    remaining.remove(par1[index])
                    child_row2[index] = par1[index]
                    next = par2[index]

                cycle += 1

        return child_row1, child_row2

    
    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if (parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if (parent_row[i] == value):
                return i