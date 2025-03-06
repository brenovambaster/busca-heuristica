import numpy as np



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

