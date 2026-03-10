from algoritmes.algoritme_cerca_local import AlgoritmeCercaLocal
from problemes.problema import ProblemaCercaLocal


class HillClimbing(AlgoritmeCercaLocal):

    def __init__(self, K, max_reinicis_sense_millora):
        """
        :param K: nombre màxim d'iteracions totals
        :param max_reinicis_sense_millora: criteri d'aturada addicional;
               si després d'aquest nombre de reinicis consecutius no s'ha
               millorat el millor cost global, l'algoritme s'atura
        """
        self.K = K
        self.max_reinicis_sense_millora = max_reinicis_sense_millora

    def executa(self, problema: ProblemaCercaLocal):
        """
        Executa el Hill Climbing amb reinici aleatori sobre el problema donat.

        Criteris d'aturada:
          1. S'han fet K iteracions totals
          2. No hi ha hagut millora global en els últims max_reinicis_sense_millora reinicis

        :param problema: instància d'un ProblemaCercaLocal
        :return:
            millor_estat_global: millor estat trobat en tots els reinicis
            historic_cost: llista amb el millor cost global a cada iteració
        """
        # inicialitzem les variables globals (el millor que hem vist fins ara)
        millor_estat_global = None
        millor_cost_global = float('inf')

        # historial per pintar la gràfica després, i comptadors de control
        historic_cost = []
        iteracions_totals = 0
        reinicis_sense_millora = 0

        # bucle de reinicis: parem si exhaurim K o portem massa reinicis sense millorar
        while iteracions_totals < self.K and reinicis_sense_millora < self.max_reinicis_sense_millora:

            # guardem el cost abans per saber si aquest reinici ha servit de algo
            millor_cost_abans_reinici = millor_cost_global

            # generem un estat inicial aleatori i calculem el seu cost
            estat_actual = problema.estat_inicial()
            cost_actual = problema.cost(estat_actual)

            # comprovem si aquest estat inicial ja és millor que el global
            if cost_actual < millor_cost_global:
                millor_estat_global = estat_actual
                millor_cost_global = cost_actual
            historic_cost.append(millor_cost_global)
            iteracions_totals += 1

            # hill climbing local: ens movem sempre cap al millor veí fins a mínim local
            while iteracions_totals < self.K:

                # obtenim el veí amb menor cost
                veins = problema.veinat(estat_actual)
                millor_vei = min(veins, key=problema.cost)
                cost_millor_vei = problema.cost(millor_vei)

                # mínim local, cap veí millora l'actual, sortim del bucle intern
                if not problema.es_millor(millor_vei, estat_actual):
                    break

                # ens movem al millor veí
                estat_actual = millor_vei
                cost_actual = cost_millor_vei

                # actualitzem el millor global si hem millorat
                if cost_actual < millor_cost_global:
                    millor_estat_global = estat_actual
                    millor_cost_global = cost_actual

                historic_cost.append(millor_cost_global)
                iteracions_totals += 1

            # comprovem si aquest reinici ha aportat millora global o no
            if millor_cost_global < millor_cost_abans_reinici:
                reinicis_sense_millora = 0
            else:
                reinicis_sense_millora += 1
            # debug
            # print(f"Reinicis sense millora en acabar: {reinicis_sense_millora}")
            # print(f"Iteracions totals: {iteracions_totals}")
        # ret
        return millor_estat_global, historic_cost