import numpy as np
import random
from itertools import product


class KMeans:
    """
    Implementação personalizada do algoritmo K-Means.
    
    Attributes:
        n_clusters (int): Número de clusters desejados.
        max_iter (int): Número máximo de iterações.
        tol (float): Tolerância para verificar a convergência.
        centroids (np.ndarray): Matriz contendo os centróides no formato (n_clusters, n_features).
        data (np.ndarray): Dados de entrada no formato (n_samples, n_features).
        labels (np.ndarray): Array contendo o índice do cluster para cada ponto.
    """
    __slots__ = ['n_clusters', 'max_iter', 'tol', 'centroids', 'data', 'labels']

    def __init__(self, n_clusters, max_iter=100, tol=1e-4, initial_centroids=None):
        """
        Construtor da classe KMeans.

        :param n_clusters: Número de clusters desejados.
        :param max_iter: Número máximo de iterações (padrão: 100).
        :param tol: Tolerância para verificação de convergência (padrão: 1e-4).
        :param initial_centroids: Centróides iniciais (opcional). Caso não fornecido,
                                  podem ser inicializados automaticamente com `fit`.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        
        # Caso sejam passados centróides iniciais, faça o cast para numpy array.
        # Caso contrário, deixe para ser inicializado no `fit`.
        self.centroids = np.array(initial_centroids) if initial_centroids is not None else None

        # Serão definidas posteriormente
        self.data = None
        self.labels = None

    def fit(self, data):
        """
        Ajusta o modelo K-Means aos dados fornecidos.

        :param data: Dados de entrada no formato (n_amostras, n_features).
        :return: Retorna a instância do próprio objeto (self).
        """
        self.data = data
        n_samples, _ = data.shape

        # Se os centróides não foram definidos manualmente, inicializa aleatoriamente.
        if self.centroids is None:
            # Escolhe n_clusters amostras aleatórias como centróides iniciais
            idx = np.random.choice(n_samples, self.n_clusters, replace=False)
            self.centroids = data[idx, :]

        for _ in range(self.max_iter):
            # Atribui cada ponto ao cluster mais próximo
            self.labels = np.array([self._closest_centroid(point) for point in data])

            # Atualiza os centróides baseados na média dos pontos pertencentes a cada cluster
            new_centroids = np.array([
                data[self.labels == i].mean(axis=0) if np.any(self.labels == i) else self.centroids[i] 
                for i in range(self.n_clusters)
            ])

            # Checa a convergência pela norma da diferença entre antigos e novos centróides
            shift = np.linalg.norm(new_centroids - self.centroids)
            self.centroids = new_centroids
            if shift < self.tol:
                break

        return self

    def _closest_centroid(self, point):
        """
        Calcula o índice do centróide mais próximo de um ponto.

        :param point: Ponto de dados.
        :return: Índice do centróide mais próximo.
        """
        distances = np.linalg.norm(self.centroids - point, axis=1)
        return np.argmin(distances)
    
    def compute_cost(self):
        """
        Calcula a soma das distâncias dos pontos aos seus centróides.

        :return: Custo total (soma das distâncias).
        """
        if self.labels is None:
            raise ValueError("O modelo não foi ajustado. Chame o método `fit` antes de calcular o custo.")
        distances = np.linalg.norm(self.data - self.centroids[self.labels], axis=1)
        return np.sum(distances)
    
    def compute_average_cost(self):
        """
        Calcula a distância média dos pontos aos seus centróides.

        :return: Média das distâncias.
        """
        if self.labels is None:
            raise ValueError("O modelo não foi ajustado. Chame o método `fit` antes de calcular a distância média.")
        distances = np.linalg.norm(self.data - self.centroids[self.labels], axis=1)
        return np.mean(distances)


def compute_total_distance(data, centroids):
    """
    Calcula a soma das distâncias dos pontos aos seus centróides mais próximos.

    :param data: Dados no formato (n_samples, n_features).
    :param centroids: Centróides no formato (n_centroids, n_features).
    :return: Soma das distâncias.
    """
    # Para cada ponto, calcule a distância até todos os centróides e pegue a menor
    distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    min_distances = np.min(distances, axis=1)
    return np.sum(min_distances)


def local_search(data, centroids, neighbors, mode="best"):
    """
    Realiza a busca local para encontrar uma configuração melhor de centróides.

    :param data: Dados de entrada no formato (n_samples, n_features).
    :param centroids: Centróides iniciais (n_clusters, n_features).
    :param neighbors: Array contendo vizinhanças de cada centróide
                      no formato (n_centroids, n_neighbors, n_features).
    :param mode: Estratégia de busca local:
                 - 'first' para primeira melhora,
                 - 'best' para melhor melhora.
    :return: Uma tupla contendo:
        - best_centroids (np.ndarray): Melhor configuração de centróides.
        - best_cost (float): Menor soma de distâncias encontrada.
        - history (list): Histórico de custos durante a busca.
    """
    if mode not in ("first", "best"):
        raise ValueError("Modo inválido. Use 'first' ou 'best'.")
    
    if not isinstance(neighbors, np.ndarray) or neighbors.ndim != 3:
        raise ValueError("O array de vizinhanças deve ter formato (n_centroids, n_neighbors, n_features).")
    
    # Custo e configuração inicial
    best_centroids = centroids.copy()
    best_cost = compute_total_distance(data, centroids)
    history = [best_cost]

    # Gera todas as combinações possíveis de vizinhança (cartesian product)
    neighbor_combinations = list(product(*[neighbors[i] for i in range(neighbors.shape[0])]))
    
    
    # Embaralha a lista de combinações para evitar viés de ordem
    random.shuffle(neighbor_combinations)

    if mode == "first":
        return _local_search_first(data, best_centroids, neighbor_combinations, best_cost, history)
    else:  # mode == "best"
        return _local_search_best(data, best_centroids, neighbor_combinations, best_cost, history)


def _local_search_first(data, centroids, neighbor_combinations, best_cost, history):
    """
    Realiza a busca local no modo 'first', retornando na primeira melhora encontrada.

    :param data: Dados de entrada.
    :param centroids: Centróides iniciais.
    :param neighbor_combinations: Lista de todas as combinações possíveis de vizinhança.
    :param best_cost: Custo da melhor configuração atual.
    :param history: Histórico de custos até o momento.
    :return: Tupla (best_centroids, best_cost, history).
    """
    best_centroids = centroids.copy()

    for combination in neighbor_combinations:
        candidate_centroids = np.array(combination)
        candidate_cost = compute_total_distance(data, candidate_centroids)
        history.append(candidate_cost)

        if candidate_cost < best_cost:
            return candidate_centroids, candidate_cost, history  # Retorna na primeira melhora
    
    # Se não houver melhora, retorna a configuração atual
    return best_centroids, best_cost, history


def _local_search_best(data, centroids, neighbor_combinations, best_cost, history):
    """
    Realiza a busca local no modo 'best', avaliando todas as combinações de vizinhos.

    :param data: Dados de entrada.
    :param centroids: Centróides iniciais.
    :param neighbor_combinations: Lista de todas as combinações possíveis de vizinhança.
    :param best_cost: Custo da melhor configuração atual.
    :param history: Histórico de custos até o momento.
    :return: Tupla (best_centroids, best_cost, history).
    """
    best_centroids = centroids.copy()

    for combination in neighbor_combinations:
        candidate_centroids = np.array(combination)
        candidate_cost = compute_total_distance(data, candidate_centroids)
        history.append(candidate_cost)

        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_centroids = candidate_centroids

    return best_centroids, best_cost, history
