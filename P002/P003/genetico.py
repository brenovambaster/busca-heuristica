import numpy as np
import random
from typing import List, Optional, Tuple

class Individual:
    """
    Representa um indivíduo na população, isto é, uma configuração de centróides.
    Cada indivíduo armazena seus centróides e o fitness associado.
    """

    def __init__(self, centroids: np.ndarray):
        self.centroids = centroids
        self.fitness: Optional[float] = None

    def evaluate(self, data: np.ndarray) -> None:
        """
        Calcula o fitness do indivíduo com base na soma das distâncias dos pontos
        aos respectivos centróides mais próximos.
        """
        labels = np.array([self._closest_centroid(point) for point in data])
        distances = np.linalg.norm(data - self.centroids[labels], axis=1)
        self.fitness = float(np.sum(distances))

    def _closest_centroid(self, point: np.ndarray) -> int:
        """
        Retorna o índice do centróide mais próximo de um dado ponto.
        """
        distances = np.linalg.norm(self.centroids - point, axis=1)
        return int(np.argmin(distances))

class GeneticAlgorithm:
    """
    Implementação de um algoritmo genético para otimização de centróides do K-Means.

    Etapas:
    1. Inicialização da população.
    2. Avaliação do fitness.
    3. Seleção dos indivíduos (torneio ou roleta).
    4. Crossover.
    5. Mutação.
    6. Elitismo e reprodução.
    7. Critérios de parada.
    """

    def __init__(
        self,
        data: np.ndarray,
        n_clusters: int,
        population_size: int,
        generations: int,
        mutation_rate: float,
        elite_size: int = 2,
        selection_method: str = "tournament",  # Pode ser 'tournament' ou 'roulette'
    ):
        """
        :param data: Dados de entrada (n_samples, n_features).
        :param n_clusters: Número de clusters.
        :param population_size: Tamanho da população.
        :param generations: Número de gerações.
        :param mutation_rate: Taxa de mutação.
        :param elite_size: Quantidade de indivíduos que serão mantidos por elitismo.
        :param selection_method: Método de seleção ('tournament' ou 'roulette').
        """
        self.data = data
        self.n_clusters = n_clusters
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.selection_method = selection_method
        self.population: List[Individual] = []

    def initialize_population(self, initial_solutions: Optional[List[np.ndarray]] = None) -> None:
        """
        Inicializa a população. Caso sejam fornecidas soluções iniciais (por exemplo, vindas da Busca Tabu),
        elas são adicionadas à população. Em seguida, a população é completada com indivíduos aleatórios.
        """
        self.population = []
        if initial_solutions:
            for sol in initial_solutions:
                self.population.append(Individual(sol))

        while len(self.population) < self.population_size:
            random_indices = np.random.choice(len(self.data), self.n_clusters, replace=False)
            random_centroids = self.data[random_indices]
            self.population.append(Individual(random_centroids))

    def evaluate_population(self) -> None:
        """
        Avalia o fitness de todos os indivíduos na população.
        """
        for individual in self.population:
            individual.evaluate(self.data)

    def select_parents(self) -> Tuple[Individual, Individual]:
        """
        Seleciona dois indivíduos para reprodução, de acordo com o método escolhido.
        Disponibiliza o "tournament" ou a "roulette".
        """
        if self.selection_method == "tournament":
            return self._tournament_selection()
        else:
            return self._roulette_selection()

    def _tournament_selection(self, k: int = 3) -> Tuple[Individual, Individual]:
        """
        Método de seleção por torneio. Seleciona aleatoriamente k indivíduos
        e escolhe o melhor (menor fitness) entre eles. Repete para escolher os dois pais.
        """
        parent1 = self._tournament_pick(k)
        parent2 = self._tournament_pick(k)
        return parent1, parent2

    def _tournament_pick(self, k: int) -> Individual:
        tournament = random.sample(self.population, k)
        # Ordena por fitness, pois menor fitness é melhor.
        tournament.sort(key=lambda ind: ind.fitness)
        return tournament[0]

    def _roulette_selection(self) -> Tuple[Individual, Individual]:
        """
        Método de seleção por roleta: a probabilidade de seleção é inversamente proporcional ao fitness.
        """
        # Primeiro, precisamos do inverso do fitness (porque fitness menor é melhor)
        fitness_values = [ind.fitness for ind in self.population]
        max_fit = max(fitness_values)
        # Convertendo para valores de aptidão em que maior é melhor:
        inverted_fitness = [max_fit - f for f in fitness_values]
        total = sum(inverted_fitness)

        parent1 = self._roulette_pick(inverted_fitness, total)
        parent2 = self._roulette_pick(inverted_fitness, total)
        return parent1, parent2

    def _roulette_pick(self, inverted_fitness: List[float], total: float) -> Individual:
        r = random.random() * total
        cumulative = 0.0
        for i, ind in enumerate(self.population):
            cumulative += inverted_fitness[i]
            if cumulative >= r:
                return ind
        return self.population[-1]

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """
        Crossover que troca parte dos centróides entre dois pais.
        """
        mask = np.random.rand(self.n_clusters) > 0.5
        # Aplica a máscara para escolher centróides do parent1 ou parent2
        new_centroids = np.where(mask[:, None], parent1.centroids, parent2.centroids)
        return Individual(new_centroids)

    def mutate(self, individual: Individual) -> None:
        """
        Aplica mutação aos centróides do indivíduo, alterando um centróide de forma aleatória.
        """
        if random.random() < self.mutation_rate:
            # Escolhe um centróide aleatório para mutar
            mutation_idx = np.random.randint(self.n_clusters)
            # Perturbação gaussiana
            individual.centroids[mutation_idx] += np.random.normal(0, 0.1, size=individual.centroids.shape[1])

    def evolve(self) -> Individual:
        """
        Executa o loop principal do algoritmo genético e retorna o melhor indivíduo.
        """
        # Avalia a população inicial
        self.evaluate_population()

        for _ in range(self.generations):
            # Ordena a população por fitness (crescente)
            self.population.sort(key=lambda ind: ind.fitness)

            # Elitismo: mantém os melhores
            next_population = self.population[: self.elite_size]

            # Preenche o restante da população
            while len(next_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                offspring = self.crossover(parent1, parent2)
                self.mutate(offspring)
                offspring.evaluate(self.data)
                next_population.append(offspring)

            self.population = next_population

        # Ao final, retorna o melhor indivíduo
        self.population.sort(key=lambda ind: ind.fitness)
        return self.population[0]


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo simples
    np.random.seed(42)
    data = np.random.rand(100, 2)
    n_clusters = 3

    # Suponha que tenhamos algumas "soluções boas" (por ex. da Busca Tabu)
    # Aqui, por exemplo, vamos usar algumas matrizes de centróides arbitrárias.
    good_solutions = [
        np.array([[0.2, 0.15], [-1.0, -1.0], [1.1, 1.1]]),
        np.array([[0.25, 0.18], [-1.1, -0.9], [1.2, 1.2]])
    ]

    ga = GeneticAlgorithm(
        data=data,
        n_clusters=n_clusters,
        population_size=20,
        generations=50,
        mutation_rate=0.1,
        elite_size=2,
        selection_method="tournament",
    )

    ga.initialize_population(initial_solutions=good_solutions)
    best_individual = ga.evolve()
    print("Melhores centróides:", best_individual.centroids)
    print("Fitness:", best_individual.fitness)
