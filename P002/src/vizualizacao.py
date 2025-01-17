import matplotlib.pyplot as plt

def plot_kmeans_results(data, centroids, labels):
    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap="viridis", alpha=0.6)
    plt.scatter(centroids[:, 0], centroids[:, 1], color="red", marker="X")
    plt.title("Resultados do K-Means")
    plt.show()