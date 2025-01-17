import numpy as np
import random
import pandas as pd
from itertools import product

class KMeans:
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
        self.centroids = data[np.random.choice(n_samples, self.n_clusters, replace=False)]

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



def local_search(data, centroids, neighbors, mode="best"):
    """
    Realiza a busca local para encontrar uma configuração melhor de centróides.

    Args:
        data (np.ndarray): Dados de entrada (n_samples, n_features).
        centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (np.ndarray): Array contendo vizinhanças de cada centróide.
        mode (str): 'first' para primeira melhora, 'best' para melhor melhora.

    Returns:
        tuple: Melhor configuração de centróides e a menor soma de distâncias.
    """
    if mode not in ["first", "best"]:
        raise ValueError("Modo inválido. Use 'first' ou 'best'.")
    
    # Calcula o custo inicial
    best_centroids = centroids
    best_cost = compute_total_distance(data, centroids)
    
    if mode == "first":
        # Estratégia de primeira melhora
        for i, centroid_neighbors in enumerate(neighbors):
            for neighbor in centroid_neighbors:
                new_centroids = centroids.copy()
                new_centroids[i] = neighbor  # Substitui o centróide por seu vizinho
                new_cost = compute_total_distance(data, new_centroids)
                
                if new_cost < best_cost:
                    return new_centroids, new_cost  # Retorna na primeira melhora encontrada

    elif mode == "best":
        # Estratégia de melhor melhora
        for i, centroid_neighbors in enumerate(neighbors):
            for neighbor in centroid_neighbors:
                new_centroids = centroids.copy()
                new_centroids[i] = neighbor  # Substitui o centróide por seu vizinho
                new_cost = compute_total_distance(data, new_centroids)
                
                if new_cost < best_cost:
                    best_centroids = new_centroids
                    best_cost = new_cost
    
    return best_centroids, best_cost



def local_search_with_history(data, initial_centroids, neighbors, mode="first"):
    """
    Realiza busca local para minimizar o custo, com histórico para análise.

    Args:
        data (np.ndarray): Dados (n_samples, n_features).
        initial_centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (list): Vizinhanças dos centróides.
        mode (str): 'first' para a primeira melhora, 'best' para a melhor melhora.

    Returns:
        tuple: (melhores centróides, custo final, histórico de custos).
    """
    # Converter para arrays NumPy se necessário
    if isinstance(data, pd.DataFrame):
        data = data.values
    if isinstance(initial_centroids, pd.DataFrame):
        initial_centroids = initial_centroids.values

    # Garantir que os dados são 2D
    data = np.atleast_2d(data)
    initial_centroids = np.atleast_2d(initial_centroids)

    current_centroids = initial_centroids.copy()
 
    current_cost = compute_total_distance(data, current_centroids)
    history = [current_cost]

    improved = True

    while improved:
        improved = False
        for i, centroid_neighbors in enumerate(neighbors):
            best_neighbor = None
            best_cost = current_cost

            for neighbor in centroid_neighbors:
                candidate_centroids = current_centroids.copy()
                candidate_centroids[i] = neighbor
                candidate_cost = compute_total_distance(data, candidate_centroids)

                if candidate_cost < current_cost:
                    if mode == "first":
                        current_centroids = candidate_centroids
                        current_cost = candidate_cost
                        history.append(current_cost)
                        improved = True
                        break
                    elif mode == "best":
                        if candidate_cost < best_cost:
                            best_neighbor = neighbor
                            best_cost = candidate_cost

            if mode == "best" and best_neighbor is not None:
                current_centroids[i] = best_neighbor
                current_cost = best_cost
                history.append(current_cost)
                improved = True

            if improved and mode == "first":
                break

    return current_centroids, current_cost, history
