import numpy as np

def generate_neighbors(centroids, delta, N_PASSOS=1):
    """
    Gera uma lista de vizinhanças para cada centróide.

    Args:
        centroids (np.ndarray): Array de centróides no formato (n_centroids, n_features).
        delta (float): Incremento para gerar vizinhanças.
        N_PASSOS (int): Número de passos extras em cada direção.

    Returns:
        np.ndarray: Array contendo vizinhanças de cada centróide no formato
                    (n_centroids, n_neighbors, n_features).
    """
    if not isinstance(centroids, np.ndarray):
        raise ValueError("Os centróides devem ser um np.ndarray.")
    if not isinstance(delta, (int, float)):
        raise ValueError("Delta deve ser um número.")
    if not isinstance(N_PASSOS, int) or N_PASSOS <= 0:
        raise ValueError("N_PASSOS deve ser um inteiro positivo.")

    # Determinar os deslocamentos para gerar vizinhanças
    steps = [delta * i for i in range(-N_PASSOS, N_PASSOS + 1)]

    # Gerar vizinhanças para cada centróide
    neighbors = []
    for centroid in centroids:
        centroid_neighbors = set()  # Usar set para evitar duplicatas
        for displacement in np.ndindex(*([len(steps)] * centroids.shape[1])):
            offset = np.array([steps[i] for i in displacement])
            new_neighbor = tuple(centroid + offset)
            if not np.allclose(offset, 0):  # Evitar o próprio centróide
                centroid_neighbors.add(new_neighbor)
        neighbors.append(np.array(list(centroid_neighbors)))

    return np.array(neighbors)
