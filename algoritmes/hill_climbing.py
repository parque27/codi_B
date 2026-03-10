from algoritmes.algoritme_cerca_local import AlgoritmeCercaLocal
from problemes.problema import ProblemaCercaLocal


class HillClimbing(AlgoritmeCercaLocal):

    def __init__(self, K=500, max_reinicis_sense_millora=50):
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
            historic_cost: llista amb el millor cost global after de cada iteració
        """

        # Inicialitzem el millor estat global com a None
        millor_estat_global = None
        millor_cost_global = float('inf')  # Infinit, ja que volem minimitzar

        historic_cost = []          # Historial del millor cost global a cada iteració
        iteracions_totals = 0       # Comptador d'iteracions totals
        reinicis_sense_millora = 0  # Comptador de reinicis consecutius sense millora global

        # Bucle principal: reinicis aleatoris
        while iteracions_totals < self.K and reinicis_sense_millora < self.max_reinicis_sense_millora:

            # --- INICI D'UN NOU REINICI ---

            # Partim d'un estat inicial aleatori en cada reinici
            estat_actual = problema.estat_inicial()
            cost_actual = problema.cost(estat_actual)

            # Actualitzem el millor global si cal i afegim a l'historial
            if cost_actual < millor_cost_global:
                millor_estat_global = estat_actual
                millor_cost_global = cost_actual
            historic_cost.append(millor_cost_global)
            iteracions_totals += 1

            # --- HILL CLIMBING LOCAL (fins a mínim local o exhaurir K) ---
            while iteracions_totals < self.K:

                # Obtenim tots els veïns de l'estat actual
                veins = problema.veinat(estat_actual)

                # Trobem el millor veí (mínim cost, ja que és minimització)
                millor_vei = min(veins, key=problema.cost)
                cost_millor_vei = problema.cost(millor_vei)

                # Si el millor veí no millora l'estat actual, mínim local assolit
                # Aturem el hill climbing local i fem un nou reinici
                if not problema.es_millor(millor_vei, estat_actual):
                    break

                # Ens movem al millor veí
                estat_actual = millor_vei
                cost_actual = cost_millor_vei

                # Actualitzem el millor global si aquest veí és millor
                if cost_actual < millor_cost_global:
                    millor_estat_global = estat_actual
                    millor_cost_global = cost_actual

                # Afegim el millor cost global actual a l'historial
                historic_cost.append(millor_cost_global)
                iteracions_totals += 1

            # --- ACTUALITZEM EL COMPTADOR DE REINICIS SENSE MILLORA ---

            # Si aquest reinici no ha millorat el millor global, incrementem el comptador
            if cost_actual >= millor_cost_global:
                reinicis_sense_millora += 1
            else:
                reinicis_sense_millora = 0

        return millor_estat_global, historic_cost