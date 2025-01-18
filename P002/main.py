import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from src.preprocessamento import preprocess_data
from src.utils import generate_neighbors
from src.algoritmos import *
from src.vizualizacao import plot_kmeans_results
from src.tabu import *
from tabulate import tabulate

#----------------------------------------------------------
# Função principal de execução
def main():
    """
    Função principal para executar o pipeline completo, incluindo o K-Means,
    busca local (primeira e melhor melhora) e busca tabu.
    """
    # Resultados armazenados para a tabela
    resultados = []

    # Carregar e preparar os dados
    data = load_data("data/wine.data")
    features = ['Flavanoids', 'Total_Phenols']
    reduced_data, scaler = preprocess_data(data, features)

    # Executar K-Means
    kmeans = execute_kmeans(reduced_data, n_clusters=3)
    resultados.append(["K-Means", kmeans.centroids.tolist(), kmeans.cost()])
    print("Custo total do K-Means:", kmeans.cost())
    print_separator()

    # Gerar vizinhanças dos centróides
    neighbors = generate_neighbors(kmeans.centroids, delta=0.1, N_PASSOS=3)

    # Realizar a busca local (primeira melhora)
    neighbors_local = neighbors.copy()
    random.shuffle(neighbors_local)
    first_centroids, first_distance = local_search(
        reduced_data, kmeans.centroids, neighbors_local, mode="first"
    )
    resultados.append(["Busca Local (Primeira Melhora)", first_centroids.tolist(), first_distance])
    print("Primeiros centróides encontrados:", first_centroids)
    print("Custo total da busca local (primeira melhora):", first_distance)
    print_separator()

    # Realizar a busca local (melhor melhora)
    best_centroids, best_distance = local_search(
        reduced_data, kmeans.centroids, neighbors_local, mode="best"
    )
    resultados.append(["Busca Local (Melhor Melhora)", best_centroids.tolist(), best_distance])
    print("Melhores centróides encontrados:", best_centroids)
    print("Custo total da busca local (melhor melhora):", best_distance)
    print_separator()

    # Busca local com histórico
    neighbors_h1 = neighbors.copy()
    random.shuffle(neighbors_h1)

    centroids_first, cost_first, history_first = local_search_with_history(
        reduced_data, kmeans.centroids, neighbors_h1, mode="first"
    )

    centroids_best, cost_best, history_best = local_search_with_history(
        reduced_data, kmeans.centroids, neighbors_h1, mode="best"
    )

    # Visualizar resultados
    plot_results(reduced_data, kmeans, centroids_best, history_first, history_best)

    # Busca tabu
    neighbors_tabu = neighbors.copy()
    best_centroids_tabu, best_cost_tabu, history_tabu = tabu_search(
        reduced_data, kmeans.centroids, neighbors_tabu, max_iter=150, tabu_size=8
    )
    resultados.append(["Busca Tabu", best_centroids_tabu.tolist(), best_cost_tabu])
    print("Melhores centróides pela busca tabu:", best_centroids_tabu)
    print("Custo final da busca tabu:", best_cost_tabu)
    print_separator()

    # Plotar histórico da busca tabu
    plt.figure(figsize=(10, 6))
    plt.plot(history_tabu, label="Busca Tabu", marker="o")
    plt.xlabel("Iteração")
    plt.ylabel("Custo")
    plt.title("Histórico da Busca Tabu")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Exibir tabela de resultados
    print( "\n## RESUMO DOS RESULTADOS ##\n")
    mostrar_tabela_resultados(resultados)

#----------------------------------------------------------
# Função para carregar dados
def load_data(file_path):
    """
    Carrega os dados a partir de um arquivo CSV e define os nomes das colunas.

    Parâmetros:
        file_path (str): Caminho para o arquivo CSV.

    Retorno:
        pd.DataFrame: DataFrame com os dados carregados.
    """
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
    """
    Executa o algoritmo K-Means nos dados fornecidos.

    Parâmetros:
        data (pd.DataFrame ou np.ndarray): Dados de entrada.
        n_clusters (int): Número de clusters desejados.

    Retorno:
        KMeans: Objeto KMeans com os resultados do agrupamento.
    """
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    print("Centroides encontrados pelo K-Means:", kmeans.centroids)
    return kmeans

#----------------------------------------------------------
# Função para plotar resultados
def plot_results(reduced_data, kmeans, centroids_best, history_first, history_best):
    """
    Plota os resultados do K-Means, busca local e histórico de custos.

    Parâmetros:
        reduced_data (np.ndarray): Dados reduzidos para visualização.
        kmeans (KMeans): Objeto KMeans com os resultados do agrupamento.
        centroids_best (np.ndarray): Centróides da busca local (melhor melhora).
        history_first (list): Histórico de custos da busca local (primeira melhora).
        history_best (list): Histórico de custos da busca local (melhor melhora).
    """
    # Plotar resultados do K-Means
    plot_kmeans_results(reduced_data, kmeans.centroids, kmeans.labels)

    # Plotar os centróides da busca local (melhor melhora)
    plt.scatter(centroids_best[:, 0], centroids_best[:, 1], c='red', marker='X', label='Centróides Busca Local (Melhor Melhora)')

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
    plt.plot(history_best, label="Melhor Melhora", marker="s", linestyle="--", linewidth=0.8)
    plt.xlabel("Iteração")
    plt.ylabel("Custo")
    plt.title("Comparação de Desempenho: Primeira Melhora vs. Melhor Melhora")
    plt.legend()
    plt.grid(True)
    plt.show()

#----------------------------------------------------------
# Função para imprimir separador visual
def print_separator():
    """Imprime uma linha de separação para visualização."""
    print("-" * 60)

def mostrar_tabela_resultados(resultados):
    """
    Exibe uma tabela com os resultados resumidos.

    Parâmetros:
        resultados (list): Lista de listas contendo os dados dos métodos, centróides e custos.
    """
    headers = ["Método", "Centróides Encontrados", "Custo Total"]
    print(tabulate(resultados, headers=headers, tablefmt="grid"))

#----------------------------------------------------------
# Execução do programa
if __name__ == "__main__":
    main()
