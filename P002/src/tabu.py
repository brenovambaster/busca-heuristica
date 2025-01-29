import numpy as np
from itertools import product
from src.utils import generate_neighbors

def compute_total_distance(data, centroids):
    """
    Calcula a soma das distâncias dos pontos aos seus centróides mais próximos.

    Args:
        data (np.ndarray): Dados de entrada, formato (n_samples, n_features).
        centroids (np.ndarray): Centróides, formato (n_clusters, n_features).

    Returns:
        float: Soma das distâncias para o conjunto de centróides fornecido.
    """
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    min_distances = np.min(distances, axis=1)
    return np.sum(min_distances)



def tabu_search(data, initial_centroids, neighbors, max_iter=100, tabu_size=100, delta=0.1, N_PASSOS=1):
    """
    Implementa a busca tabu para minimizar o custo, utilizando busca local de
    melhor melhora (best improvement) a cada iteração.

    Args:
        data (np.ndarray): Dados de entrada no formato (n_samples, n_features).
        initial_centroids (np.ndarray): Centróides iniciais (n_clusters, n_features).
        neighbors (np.ndarray): Vizinhanças dos centróides (n_clusters, n_neighbors, n_features).
        max_iter (int): Número máximo de iterações (default = 100).
        tabu_size (int): Tamanho máximo da lista tabu (default = 100).
        delta (float): Parâmetro de variação para gerar novos vizinhos nas iterações subsequentes.
        N_PASSOS (int): Quantidade de passos/variações para cada centróide ao gerar nova vizinhança.

    Returns:
        tuple:
            - best_centroids (np.ndarray): Melhor conjunto de centróides encontrado.
            - best_cost (float): Menor custo total (soma das distâncias) encontrado.
            - history (list): Histórico de custos por iteração.
    """
    # Verificação básica do formato de neighbors
    if not isinstance(neighbors, np.ndarray) or neighbors.ndim != 3:
        raise ValueError("O array de vizinhanças deve ter formato (n_clusters, n_neighbors, n_features).")

    # Inicializações
    current_centroids = initial_centroids.copy()
    best_centroids = current_centroids.copy()
    best_cost = compute_total_distance(data, current_centroids)
    current_cost = best_cost
    tabu_list = []  # Lista tabu para registrar configurações recentes
    history = [best_cost]  # Histórico de custos

    for iter_idx in range(max_iter):
        # 1) Busca local: melhor melhora levando em conta a lista tabu
        best_candidate, best_candidate_cost = _best_improvement_search(
            data, neighbors, current_centroids, best_cost, tabu_list
        )

        # 2) Atualiza a solução corrente caso um candidato tenha sido encontrado
        if best_candidate is not None:
            current_centroids = best_candidate
            current_cost = best_candidate_cost

            # Adiciona a nova solução na lista tabu
            tabu_list.append(current_centroids.tolist())
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)  # Remove o mais antigo se exceder tamanho

            # Atualiza a melhor solução global se houver melhora
            if current_cost < best_cost:
                best_centroids = current_centroids.copy()
                best_cost = current_cost

       
        # 3) Armazena o custo da iteração no histórico
        history.append(current_cost)

        # 4) Gera nova vizinhança baseada nos centróides atuais
        neighbors = generate_neighbors(current_centroids, delta=delta, N_PASSOS=N_PASSOS)

    return best_centroids, best_cost, history


def _best_improvement_search(data, neighbors, global_best_cost, tabu_list):
    """
    Realiza a busca local “melhor melhora” (best improvement), avaliando todas
    as combinações de vizinhos, respeitando a lista tabu e aspiração.

    Args:
        data (np.ndarray): Dados de entrada.
        neighbors (np.ndarray): Vizinhanças (n_clusters, n_neighbors, n_features).
        current_centroids (np.ndarray): Centróides da solução corrente.
        global_best_cost (float): Melhor custo global conhecido (usado na aspiração).
        tabu_list (list): Lista tabu, contendo configurações recentemente visitadas.

    Returns:
        tuple:
            - best_candidate (np.ndarray or None): Melhor candidato encontrado
              ou None se nenhum satisfizer as condições.
            - best_candidate_cost (float): Custo do melhor candidato (ou inf se None).
    """
    best_candidate = None
    best_candidate_cost = float('inf')

    # Cria todas as combinações dos vizinhos (produto cartesiano)
    neighbor_combinations = list(product(*[neighbors[i] for i in range(neighbors.shape[0])]))

    for combination in neighbor_combinations:
        candidate_centroids = np.array(combination)
        candidate_cost = compute_total_distance(data, candidate_centroids)

        # Critério de aspiração: se a solução melhora global_best_cost,
        # ela pode ser escolhida mesmo se estiver na lista tabu.
        # Caso contrário, deve estar fora da tabu_list.
        if candidate_cost < global_best_cost or candidate_centroids.tolist() not in tabu_list:
            # Verifica se este candidato é a melhor opção até agora
            if candidate_cost < best_candidate_cost:
                best_candidate = candidate_centroids.copy()
                best_candidate_cost = candidate_cost

    return best_candidate, best_candidate_cost
