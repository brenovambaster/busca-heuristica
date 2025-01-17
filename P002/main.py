import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.preprocessamento import preprocess_data
from src.utils import generate_neighbors
from src.algoritmos import KMeans, local_search, local_search_with_history
from src.vizualizacao import plot_kmeans_results

#----------------------------------------------------------
# Função principal de execução
def main():
    # Carregar e preparar os dados
    data = load_data("data/wine.data")
    features = ['Flavanoids', 'Total_Phenols']
    reduced_data, scaler = preprocess_data(data, features)
    
    # Executar K-Means
    kmeans = execute_kmeans(reduced_data, n_clusters=3)
    
    # Gerar vizinhanças dos centróides
    neighbors = generate_neighbors(kmeans.centroids, delta=0.1, N_PASSOS=1)
    
    # Realizar a busca local (melhor melhora)
    best_centroids, best_distance = local_search(reduced_data, kmeans.centroids, neighbors, mode="best")
    print("Melhores centróides encontrados:", best_centroids)
    print("Menor distância total:", best_distance)
    
    # Realizar busca local com histórico
    centroids_first, cost_first, history_first = local_search_with_history(reduced_data, kmeans.centroids, neighbors, mode="first")
    centroids_best, cost_best, history_best = local_search_with_history(reduced_data, kmeans.centroids, neighbors, mode="best")

    # Visualizar resultados
    plot_results(reduced_data, kmeans, centroids_best, history_first, history_best)


#----------------------------------------------------------
# Função para carregar dados
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = [
        'Class', 'Alcohol', 'Malic_Acid', 'Ash', 'Alcalinity_of_Ash',
        'Magnesium', 'Total_Phenols', 'Flavanoids', 'Nonflavanoid_Phenols',
        'Proanthocyanins', 'Color_Intensity', 'Hue',
        'OD280/OD315_of_Diluted_Wines', 'Proline'
    ]
    return data


#----------------------------------------------------------
# Função para executar o K-Means
def execute_kmeans(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    print("Centroides encontrados pelo K-Means:", kmeans.centroids)
    return kmeans


#----------------------------------------------------------
# Função para plotar resultados
def plot_results(reduced_data, kmeans, centroids_best, history_first, history_best):
    # Plotar resultados do K-Means
    plot_kmeans_results(reduced_data, kmeans.centroids, kmeans.labels)
    
    # Plotar os centróides da busca local (melhor melhora)
    plt.scatter(centroids_best[:, 0], centroids_best[:, 1], c='red', marker='X', label='Centróides Busca Local (Melhor Melhor)')
    
    # Plotar os centróides do K-Means
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c='blue', marker='o', label='Centróides K-Means')
    
    plt.xlabel("Flavanoids")
    plt.ylabel("Total_Phenols")
    plt.title("Comparação de Centróides: K-Means vs. Busca Local (Melhor Melhora)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plotar comparação de desempenho
    plt.figure(figsize=(10, 6))
    plt.plot(history_first, label="Primeira Melhora", marker="o")
    plt.plot(history_best, label="Melhor Melhora", marker="s")
    plt.xlabel("Iteração")
    plt.ylabel("Custo")
    plt.title("Comparação de Desempenho: Primeira Melhora vs. Melhor Melhora")
    plt.legend()
    plt.grid(True)
    plt.show()


#----------------------------------------------------------
# Execução do programa
if __name__ == "__main__":
    main()
