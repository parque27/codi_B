import random
import numpy as np

from problemes.el_meu_problema import ElMeuProblema
from algoritmes.hill_climbing import HillClimbing

def main():
    np.random.seed(31)
    random.seed(31)

    n = 30

    """ DEFINICIO DEL PROBLEMA """

    costos_unitaris = [random.randint(1, 10) for _ in range(n)]
    penal_parelles = {}
    for _ in range(n): # n parelles sobre n*(n-1)/2
        i, j = random.sample(range(n), 2)
        penal_parelles[(i, j)] = random.randint(5, 20)

    problema = ElMeuProblema(n=n, costs_unitaris=costos_unitaris,
                             penal_parelles=penal_parelles,
                             nombre_ideal=10, alpha=2.0)


    """ EXECUTA ALGORITME """

    algo = HillClimbing()
    solucio, historic_cost = algo.executa(problema)

    print("Solució:",solucio)
    print("Cost final:", historic_cost[-1])

    print("Num. iterations:", len(historic_cost))
    print("Històric de cost:", historic_cost)


if __name__ == "__main__":
    main()