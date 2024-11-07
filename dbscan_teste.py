from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar e pré-processar os dados
df = pd.read_csv('data/data_janeiro.csv', delimiter=';')
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Normalizar as colunas (Latitude, Longitude e Ovos)
coords = df[['Latitude', 'Longitude']].values
ovos = df['Ovos'].values.reshape(-1, 1)
data = np.hstack([coords, ovos])

# Configurar o DBSCAN
db = DBSCAN(eps=0.05, min_samples=5).fit(data)
labels = db.labels_

# Adicionar labels ao DataFrame original para identificação
df['Cluster'] = labels

# Visualizar os clusters em um gráfico 2D
plt.figure(figsize=(10, 8))
for cluster_label in set(labels):
    if cluster_label == -1:
        # Cluster -1 é considerado ruído
        color = 'black'
        label = 'Ruído'
    else:
        color = plt.cm.Spectral(cluster_label / float(max(labels) + 1))
        label = f'Cluster {cluster_label}'
    
    plt.scatter(df[df['Cluster'] == cluster_label]['Longitude'], 
                df[df['Cluster'] == cluster_label]['Latitude'],
                c=[color], label=label, s=50)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Clusters de Casos de Dengue por Quantidade de Ovos")
plt.legend()
plt.show()
