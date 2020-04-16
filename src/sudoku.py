import numpy as np
import random
import time
from population import initial_population
from chromosome import Chromosome
from known import Known
from selection import Tournament
from crossover import CycleCrossover
from brute_force import Brute
random.seed(time.time())


class Sudoku():
    def __init__(self):
        self.known = None
        return
      # Ucitavamo podatke iz datoteke
    def readInput(self, filename):
        input = open(filename, "r")
        values = np.loadtxt(input).reshape((9, 9)).astype(int)
        self.known = Known(values)
        return

    def solve(self):

        Nc = 200  # velicina populacije
        Ne = int(0.6 * Nc)  # broj onih koji idu direktno u narednu generaciju
        generation_size = 1000  # broj generacija

        mutation_rate = 0.5  # verovatnoca da se desi mutacija

        # Kreiranje inicijalne populacije
        self.initial_population = initial_population()
        self.initial_population.seed(Nc, self.known)

        pon = 0
        for generation in range(0, generation_size):

            print("Generacija %d" % generation)

            best_fitness = 0.0
            for c in range(0, Nc):
                fitness = self.initial_population.chromosomes[c].fitness
                if (fitness == 1):
                    print("Resenje pronadjeno u generaciji: " + str(generation))
                    printBoard(self.initial_population.chromosomes[c].values)
                    return generation
                if (fitness > best_fitness):
                    best_fitness = fitness

            print("Najbolji fitnes: " + str(best_fitness))
            next_population = []
            # Biranje kandidata sa najboljim fitnesom, koji direktno idu u narednu generaciju
            self.initial_population.sort()
            elites = []
            for e in range(0, Ne):
                elite = Chromosome()
                elite.values = np.copy(self.initial_population.chromosomes[e].values)
                elites.append(elite)

            for count in range(Ne, Nc, 2):
                t = Tournament()
                parent1 = t.tournament_selection_pick_one(self.initial_population.chromosomes)
                parent2 = t.tournament_selection_pick_one(self.initial_population.chromosomes)

                cc = CycleCrossover()
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=0.6)

                child1.update_fitness()
                child1.mutate(mutation_rate, self.known)
                child1.update_fitness()
                child2.update_fitness()
                child2.mutate(mutation_rate, self.known)
                child2.update_fitness()

                next_population.append(child1)
                next_population.append(child2)

            for e in range(0, Ne):
                next_population.append(elites[e])

            self.initial_population.chromosomes = next_population
            self.initial_population.update_fitness()
            self.initial_population.sort()
            if (self.initial_population.chromosomes[0].fitness != self.initial_population.chromosomes[1].fitness):
                pon = 0
            else:
                pon += 1
            #
            # Ponovna inicijalizacija populacija ako je proslo 100 generacija u kojima 2 najbolja kandidata imaju isti fitnes
            if (pon >= 100):
                self.initial_population.seed(Nc, self.known)
                pon = 0

def printBoard(values):

    for row in range(9):
        for col in range(9):
            print(values[row][col], end=' ')
            if col + 1 == 3 or col + 1 == 6:
                print(" | ", end=' ')
        if row + 1 == 3 or row + 1 == 6:
            print("\n" + "-" * 25, end=' ')
        print()
    print()
# Pokrecu se oba algoritma odredjen broj puta uz ispis podataka o samom izvrsavanju
def start_both(path,number_of_runs):
    failures, total_time, total_generations = 0, 0, 0
    best_gen, best_time = 1000, 10000
    s = Sudoku()
    s.readInput(path)
    for i in range(number_of_runs):
        start = time.time()
        gen = s.solve()
        if (gen != None):
            total_generations += gen
            if (gen < best_gen):
                best_gen = gen
            end = time.time()
            vr = end - start
            if (vr < best_time):
                best_time = vr
            total_time += (end - start)
        if (gen == None):
            failures += 1
    if (number_of_runs - failures) > 0:
        avg_time = total_time / (number_of_runs - failures)
        avg_generations = total_generations / (number_of_runs - failures)

        success_rate = (number_of_runs - failures) / number_of_runs
        print("prosecno vreme za genetski je: " + str(round(avg_time,3)) + "\nprosecan broj generacija je: " + str(
            round(avg_generations,3)) + "\nnajbolje vreme: " + str(round(best_time,3)) + "\nnajbolja generacija:" + str(
            round(best_gen,3)) + "\nprocenat uspesnosti: " + str(round(success_rate,3)))

    b = Brute()
    b.readInput(path)
    total_time = 0
    for i in range(number_of_runs):
        start = time.time()
        b.solve()
        end = time.time()
        total_time += (end - start)
    avg_time = total_time / number_of_runs
    print("prosecno vreme za brute je: " + str(round(avg_time,7)))

def genetic_algorithm(path):
    s = Sudoku()
    s.readInput(path)
    s.solve()

def brute(path):
    b = Brute()
    b.readInput(path)
    b.solve()
def main():
    for i in range(1,2):
        path = "puzzles/" + str(i) + ".txt"
        start_both(path,3)          # pokreni oba odredjen broj puta uz ispis podataka o izvrsavanju
        #genetic_algorithm(path)     # pokreni GA
        #brute(path)                # pokreni brute
if __name__ == '__main__':
    main()


