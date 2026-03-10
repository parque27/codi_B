import random
import copy
from problemes.problema import ProblemaCercaLocal

class ElMeuProblema(ProblemaCercaLocal):
    def __init__(self, n, costs_unitaris, penal_parelles, nombre_ideal, alpha):
        """
        :param n: nombre persones disponibles
        :param costs_unitaris: llista amb cost individual per cada persona
        :param penal_parelles: diccionari de parelles incompatibles i la spenalitaz
        :param nombre_ideal: numero ideal de persones a l'equip
        :param alpha: desviacio de la mida ideal
        """
        self.n = n
        self.costs_unitaris = costs_unitaris
        self.penal_parelles = penal_parelles
        self.nombre_ideal = nombre_ideal
        self.alpha = alpha

    def estat_inicial(self):
        """
        Estat inicial random
        0 vol dir no seleccionada i 1 es seleccionada
        """
        estat = []
        for i in range(self.n):
            estat.append(random.choice([0, 1]))   # 0 o 1 random
        return estat

    def veinat(self, estat):
        """
        Tots els estats que es poden obtenir canviant una persona 

        :param estat: estat actual 
        """
        veins = []
        for i in range(self.n):
            # Creo una copia profunda de l'estat per no modificar l'original
            vei = copy.deepcopy(estat)
            # Canvio el valor de la posicio i
            vei[i] = 1 - vei[i]
            veins.append(vei)
        return veins

    def cost(self, estat):
        """
        Cost total d'un estat suma de cost individual per pers seleccionada, penalitzacions de parelles incompatiles i penalitzacio per desviacio de mida ideal
        :param estat: estat a avaluar
        """
        cost_total = 0

        #Costos individuals
        for i in range(self.n):
            if estat[i] == 1: # persona seleccionada
                cost_total += self.costs_unitaris[i]

        # Penalitzacions per incompatibilitats
        for (i, j), penal in self.penal_parelles.items():
            if estat[i] == 1 and estat[j] == 1:  
                cost_total += penal

        # Desviacio de la mida ideal
        mida_actual = sum(estat)     # numero de persones seleccionades
        cost_total += self.alpha * abs(mida_actual - self.nombre_ideal)

        return cost_total