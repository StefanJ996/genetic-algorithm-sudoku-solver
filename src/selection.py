import random

class Tournament():
    def __init__(self):
        return
    # Koristimo turnirsku selekciju da izaberemo dva roditelja koja ce ucestvovati u ukrstanju
    def tournament_selection_pick_one(self, chromosomes):
        """ Biramo nasumicno 2 jedinke iz populacije i poredimo ih """
        pick1 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        pick2 = chromosomes[random.randint(0, len(chromosomes) - 1)]
        f1 = pick1.fitness
        f2 = pick2.fitness

        # Odredjujemo koja je jedina vise a koja manje prilagodjena
        if (f1 > f2):
            fittest = pick1
            weakest = pick2
        else:
            fittest = pick2
            weakest = pick1

        # ako je nas random br manji od selection rate, bira se prilagodjenija jedinka ako ne onda manje priladjena
        selection_rate = 0.85
        r = random.random()
        if (r < selection_rate):
            return fittest
        else:
            return weakest
