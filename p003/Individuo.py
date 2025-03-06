from __future__ import annotations
import numpy as np
from typing import Optional, List, Tuple

class Individuo:
    """
    Representa um indivíduo da população para o algoritmo genético aplicado ao k-means.
    
    Cada indivíduo encapsula uma solução candidata para o problema de agrupamento,
    consistindo em um conjunto de três centróides no plano cartesiano. O fitness
    do indivíduo é calculado com base na soma das distâncias mínimas entre cada
    ponto do conjunto de dados e seu centróide mais próximo.
    
    Attributes:
        individuo (np.ndarray): Array com formato (3, 1, 2) representando os três 
                               centróides, onde cada centróide é do tipo [[x, y]].
        fitness (float): Valor que quantifica a qualidade da solução (menor é melhor).
    """
    def __init__(self, *, data: np.ndarray, individuo: Optional[np.ndarray] = None) -> None:
        """
        Inicializa um indivíduo com centróides e calcula seu fitness.
        
        Args:
            data: Conjunto de dados utilizado para calcular o fitness, no formato
                 (n_samples, n_features).
            individuo: Array com formato (3, 1, 2) representando os três centróides.
                      Se None, inicializa com valores padrão que devem ser configurados
                      posteriormente.
        """
        if individuo is not None:
            self.individuo = individuo
            self.fitness = self.calculate_fitness(data)
        else:
            # Inicializa com 3 centróides com valores None (devem ser configurados posteriormente)
            self.individuo = np.array([[[None, None]],
                                       [[None, None]],
                                       [[None, None]]])
        self.data = data
        

    def set_individuo(self, individuo: np.ndarray) -> None:
        """
        Atualiza o array de centróides do indivíduo.
        
        Args:
            individuo: Novo array de centróides com formato (3, 1, 2).
                      Cada elemento representa as coordenadas de um centróide
                      no formato [[x, y]].
        """
        self.individuo = individuo
        self.fitness = self.calculate_fitness(self.data)

    def calculate_fitness(self, data: np.ndarray) -> float:
        """
        Calcula o fitness do indivíduo baseado no critério de soma das distâncias.
        
        O fitness é calculado somando as distâncias euclidianas mínimas entre
        cada ponto do conjunto de dados e o centróide mais próximo. Um valor
        menor de fitness indica uma melhor solução.
        
        Args:
            data: Conjunto de dados no formato (n_samples, n_features), onde cada
                 linha representa um ponto com coordenadas (x, y).
        
        Returns:
            O valor de fitness calculado (soma das distâncias mínimas).
        """
        # Para cada ponto, calcule a distância até todos os centróides e pegue a menor
        distances_min_acomuladas = []

        for ponto in data:
            distances = []
            for centroide in self.individuo:
                # Calcula a distância euclidiana entre o ponto e o centróide
                dist = np.linalg.norm(ponto - centroide)
                distances.append(dist)
            # Pega a menor distância (centróide mais próximo)
            distances_min_acomuladas.append(min(distances))
        
        # O fitness é a soma de todas as distâncias mínimas
        self.fitness= np.sum(distances_min_acomuladas)
        return  self.fitness
        
    def mutate(self, dmax: float, prob_mutacao: float = 0.03) -> None:
        """
        Aplica o operador de mutação aos centróides do indivíduo.
        
        A mutação permite explorar novas regiões do espaço de busca, alterando
        aleatoriamente as coordenadas dos centróides. Cada centróide tem uma
        probabilidade `prob_mutacao` de sofrer mutação, e quando ocorre, suas
        coordenadas são alteradas por um valor aleatório no intervalo [-dmax, dmax].
        
        Args:
            dmax: Valor máximo de alteração para cada coordenada durante a mutação.
            prob_mutacao: Probabilidade de mutação para cada centróide (default: 0.03).
        """
        for centroide in self.individuo:
            if np.random.rand() < prob_mutacao:
                # Adiciona um valor aleatório no intervalo [-dmax, dmax] para cada coordenada
                print(f"Mutação a se aplicada em : {self.individuo}")
                print(f"Fitness atual: {self.fitness}")
                centroide += np.random.uniform(-dmax, dmax, size=2)
                self.calculate_fitness(self.data)
                print(f"Mutação após aplicada: {self.individuo}")
                print(f"Fitness após mutação: {self.fitness}")

            

    def tolist(self) -> str:
        """
        Retorna uma representação em string dos centróides e do fitness do indivíduo.
        
        Útil para visualização, depuração e registro do estado do indivíduo.
        
        Returns:
            String formatada contendo os valores dos centróides e fitness.
        """
        return f"centroides: {self.individuo.tolist()} fitness: {self.fitness}"