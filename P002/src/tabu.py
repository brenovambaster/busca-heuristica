import numpy as np
from src.algoritmos import *
from src.utils import generate_neighbors
from itertools import product
import numpy as np

def tabu_search(data, initial_centroids, neighbors, max_iter=100, tabu_size=100):
    """
    Implementa a busca tabu para minimizar o custo.

    Args:
        data (np.ndarray): Dados de entrada no formato (n_samples, n_features).
        initial_centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (np.ndarray): Vizinhanças dos centróides (n_clusters, n_neighbors, n_features).
        max_iter (int): Número máximo de iterações.
        tabu_size (int): Tamanho máximo da lista tabu.

    Returns:
        tuple:
            - Melhor conjunto de centróides encontrado (np.ndarray).
            - Menor custo total (float).
            - Histórico de custos por iteração (list).
    """
    # Inicializações
    current_centroids = initial_centroids.copy()
    best_centroids = current_centroids.copy()
    best_cost = compute_total_distance(data, current_centroids)
    current_cost = best_cost
    tabu_list = []  # Lista tabu para registrar os centróides recentes
    history = [best_cost]  # Histórico de custos

    for iteration in range(max_iter):
        # Gerar todas as combinações de vizinhos
        neighbor_combinations = product(*[neighbors[i] for i in range(neighbors.shape[0])])
        neighbor_combinations = list(neighbor_combinations)  # Converta para lista para múltiplas iterações

        # Inicializações para a iteração atual
        best_candidate = None
        best_candidate_cost = float('inf')

        # Avaliar todas as combinações de vizinhos
        for combination in neighbor_combinations:
            candidate_centroids = np.array(combination)
            candidate_cost = compute_total_distance(data, candidate_centroids)

            # Ignorar combinações na lista tabu, a menos que atendam ao critério de aspiração
            if candidate_cost < best_cost or candidate_centroids.tolist() not in tabu_list:
                # Atualizar o melhor candidato da iteração atual
                if candidate_cost < best_candidate_cost:
                    best_candidate = candidate_centroids
                    best_candidate_cost = candidate_cost

        # Atualizar solução atual
        if best_candidate is not None:
            current_centroids = best_candidate
            current_cost = best_candidate_cost

            # Atualizar lista tabu
            tabu_list.append(current_centroids.tolist())
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            # Atualizar melhor solução global
            if current_cost < best_cost:
                best_centroids = current_centroids
                best_cost = current_cost

        # Atualizar histórico
        history.append(current_cost)

        # Gerar nova vizinhança para os centróides atuais
        neighbors = generate_neighbors(current_centroids, delta=0.1, N_PASSOS=1)

    return best_centroids, best_cost, history
