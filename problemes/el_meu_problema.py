class ElMeuProblema(ProblemaCercaLocal):
    def __init__(self, n, costs_unitaris, penal_parelles, nombre_ideal, alpha):

        self.n = n
        self.costs_unitaris = costs_unitaris
        self.penal_parelles = penal_parelles
        self.nombre_ideal = nombre_ideal
        self.alpha = alpha
    
    def estat_inicial(self):
        estat = []
        for i in range(self.n):
            estat.append(random.choice([0, 1]))
        return estat
    
    def veinat(self, estat):
        veins = []
        for i in range(self.n):
            vei = copy.deepcopy(estat);
            vei[i] = 1 - vei[i] 
            veins.append(vei)
        return veins
    
    def cost(self, estat):
        cost_total = 0
        for i in range(self.n):
            if estat[i] == 1:
                cost_total += self.costs_unitaris[i]
        
        for (i, j), penal in self.penal_parelles.items():
            if estat[i] == 1 and estat[j] == 1:
                cost_total += penal
        
        mida_actual = sum(estat)
        cost_total += self.alpha * abs(mida_actual - self.nombre_ideal)
        
        return cost_total