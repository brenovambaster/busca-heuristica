import numpy as np
import pandas as pd
from itertools import product

class KMeans:
    __slots__ = ['n_clusters', 'max_iter', 'tol', 'data', 'centroids', 'labels', 'cost_minimum']

    def __init__(self, n_clusters, max_iter=100, tol=1e-4):
        """
        Implementação personalizada do algoritmo K-Means.

        Args:
            n_clusters (int): Número de clusters desejados.
            max_iter (int): Número máximo de iterações.
            tol (float): Tolerância para verificar a convergência.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol

    def fit(self, data):
        """
        Ajusta o modelo K-Means aos dados fornecidos.

        Args:
            data (numpy.ndarray): Dados de entrada no formato (n_amostras, n_features).

        Returns:
            self: Retorna a instância ajustada.
        """
        self.data = data
        n_samples, n_features = data.shape
        # Inicializa os centróides aleatoriamente
        # self.centroids = data[np.random.choice(n_samples, self.n_clusters, replace=False)]
        self.centroids= np.array([[0.23242425, 0.16964401], 
                                  [-1.00234577, -0.99855091], 
                                  [1.11694924, 1.17118187]])

        for _ in range(self.max_iter):
            # Atribuir os pontos ao cluster mais próximo
            self.labels = np.array([self._closest_centroid(point) for point in data])

            # Atualizar os centróides
            new_centroids = np.array([data[self.labels == i].mean(axis=0) for i in range(self.n_clusters)])

            # Checar a convergência
            if np.linalg.norm(new_centroids - self.centroids) < self.tol:
                break
            self.centroids = new_centroids

        return self

    def _closest_centroid(self, point):
        """
        Calcula o centróide mais próximo de um ponto.

        Args:
            point (numpy.ndarray): Ponto de dados.

        Returns:
            int: Índice do centróide mais próximo.
        """
        distances = np.linalg.norm(self.centroids - point, axis=1)
        return np.argmin(distances)
    
    def cost(self):
        """
        Calcula a soma das distâncias dos pontos aos seus centróides mais próximos.

        Returns:
            float: Soma total das distâncias. I.e, o custo total.
        """
        distances = np.linalg.norm(self.data[:, np.newaxis] - self.centroids, axis=2)
        min_distances = np.min(distances, axis=1)
        self.cost_minimum = np.sum(min_distances)
        return np.sum(min_distances)


# Função para calcular o custo total
def compute_total_distance(data, centroids):
    """
    Calcula a soma das distâncias dos pontos aos seus centróides mais próximos.

    Args:
        data (np.ndarray): Dados no formato (n_samples, n_features).
        centroids (np.ndarray): Centróides no formato (n_centroids, n_features).

    Returns:
        float: Soma das distâncias.
    """
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    min_distances = np.min(distances, axis=1)
    return np.sum(min_distances)


from itertools import product
import numpy as np

def local_search(data, centroids, neighbors, mode="best"):
    """
    Realiza a busca local para encontrar uma configuração melhor de centróides.

    Args:
        data (np.ndarray): Dados de entrada no formato (n_samples, n_features).
        centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (np.ndarray): Array contendo vizinhanças de cada centróide
                                no formato (n_centroids, n_neighbors, n_features).
        mode (str): 'first' para primeira melhora, 'best' para melhor melhora.

    Returns:
        tuple: 
            - Melhor configuração de centróides (np.ndarray).
            - Menor soma de distâncias (float).
            - Histórico de custos (list).
    """
    if mode not in ["first", "best"]:
        raise ValueError("Modo inválido. Use 'first' ou 'best'.")
    
    if not isinstance(neighbors, np.ndarray) or neighbors.ndim != 3:
        raise ValueError("O array de vizinhanças deve ter formato (n_centroids, n_neighbors, n_features).")
    
    # Configuração inicial
    best_centroids = centroids.copy()
    best_cost = compute_total_distance(data, centroids)
    history = [best_cost]  # Histórico de custos para análise posterior

    if mode == "first":
        return _local_search_first(data, best_centroids, neighbors, best_cost, history)
    elif mode == "best":
        return _local_search_best(data, best_centroids, neighbors, best_cost, history)


def _local_search_first(data, centroids, neighbors, best_cost, history):
    """
    Realiza a busca local no modo 'first', retornando na primeira melhora encontrada.
    """
    best_centroids = centroids.copy()
    neighbor_combinations = product(*[neighbors[i] for i in range(neighbors.shape[0])])

    for combination in neighbor_combinations:
        # Cada combinação representa uma configuração completa de centróides
        candidate_centroids = np.array(combination)
        candidate_cost = compute_total_distance(data, candidate_centroids)
        # Atualizar o histórico para cada avaliação
        history.append(candidate_cost)

        # Atualizar o melhor custo e centróides, se necessário
        if candidate_cost < best_cost:
            best_centroids = candidate_centroids
            best_cost = candidate_cost
            return best_centroids, best_cost, history  # Retorna na primeira melhora encontrada
    
    return candidate_cost, best_cost, history
    


def _local_search_best(data, centroids, neighbors, best_cost, history):
    """
    Realiza a busca local no modo 'best', avaliando todas as combinações de vizinhos.
    """
    best_centroids = centroids.copy()
    neighbor_combinations = product(*[neighbors[i] for i in range(neighbors.shape[0])])

    for combination in neighbor_combinations:
        # Cada combinação representa uma configuração completa de centróides
        candidate_centroids = np.array(combination)
        candidate_cost = compute_total_distance(data, candidate_centroids)

        # Atualizar o histórico para cada avaliação
        history.append(candidate_cost)

        # Atualizar o melhor custo e centróides, se necessário
        if candidate_cost < best_cost:
            best_centroids = candidate_centroids
            best_cost = candidate_cost

    return best_centroids, best_cost, history
