import numpy as np
from src.algoritmos import *

def tabu_search(data, initial_centroids, neighbors, max_iter=100, tabu_size=5):
    """
    Implementa a busca tabu para minimizar o custo.

    Args:
        data (np.ndarray): Dados de entrada no formato (n_samples, n_features).
        initial_centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (list): Vizinhanças dos centróides.
        max_iter (int): Número máximo de iterações.
        tabu_size (int): Tamanho da lista tabu.

    Returns:
        tuple: (melhores centróides, custo final, histórico de custos).
    """
    # Configurações iniciais
    current_centroids = initial_centroids.copy()
    current_cost = compute_total_distance(data, current_centroids)
    best_centroids = current_centroids
    best_cost = current_cost
    tabu_list = []  # Lista tabu para registrar as soluções recentes
    history = [current_cost]  # Histórico de custos

    for iteration in range(max_iter):
        neighborhood_costs = []
        neighborhood_candidates = []

        # Gerar e avaliar vizinhos
        for i, centroid_neighbors in enumerate(neighbors):
            for neighbor in centroid_neighbors:
                candidate_centroids = current_centroids.copy()
                candidate_centroids[i] = neighbor
                candidate_cost = compute_total_distance(data, candidate_centroids)

                # Checa se está na lista tabu ou é melhor que o custo global
                if not is_tabu(candidate_centroids, tabu_list) or candidate_cost < best_cost:
                    neighborhood_candidates.append(candidate_centroids)
                    neighborhood_costs.append(candidate_cost)

        # Selecionar o melhor candidato
        if neighborhood_costs:
            best_index = np.argmin(neighborhood_costs)
            best_candidate = neighborhood_candidates[best_index]
            best_candidate_cost = neighborhood_costs[best_index]

            # Atualizar solução atual
            current_centroids = best_candidate
            current_cost = best_candidate_cost

            # Atualizar lista tabu
            tabu_list.append(best_candidate)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            # Atualizar melhor solução global
            if current_cost < best_cost:
                best_centroids = current_centroids
                best_cost = current_cost

            history.append(current_cost)
            print(f"Iteracao {iteration + 1}: Custo {current_cost}")
        else:
            # Se não houver vizinhos válidos, interrompe
            print("Nenhum vizinho válido encontrado.")
            break

    return best_centroids, best_cost, history


def is_tabu(candidate, tabu_list):
    """
    Verifica se um conjunto de centróides está na lista tabu.

    Args:
        candidate (np.ndarray): Solução candidata.
        tabu_list (list): Lista tabu com soluções recentes.

    Returns:
        bool: True se a solução estiver na lista tabu, False caso contrário.
    """
    for tabu in tabu_list:
        if np.allclose(candidate, tabu):
            return True
    return False
