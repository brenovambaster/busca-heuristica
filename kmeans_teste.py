from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

# Carregar seus dados reais do CSV
df = pd.read_csv('data/data_janeiro.csv', delimiter=';')  # Substitua pelo seu arquivo CSV

# Corrigir a conversão de Latitude, Longitude e Número de Ovos para o formato correto
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)
df['Ovos'] = df['Ovos'].astype(float)  # Certifique-se de que 'Ovos' seja numérico

# Definir o número de clusters
kmeans = KMeans(n_clusters=5, random_state=0).fit(df[['Latitude', 'Longitude']])

# Adicionar o rótulo do cluster ao DataFrame
df['Cluster'] = kmeans.labels_

# Definir o limiar para classificar como crítica
limiar_critico = df['Ovos'].quantile(0.75)  # Usando o 75º percentil como limiar de críticas

# Criar uma nova coluna para indicar se a região é crítica
df['Crítica'] = df['Ovos'].apply(lambda x: 'Crítica' if x >= limiar_critico else 'Não Crítica')

# Visualizar os clusters em um gráfico de dispersão, considerando o número de ovos para a cor
plt.figure(figsize=(8, 6))
scatter = plt.scatter(df['Latitude'], df['Longitude'], c=df['Ovos'], cmap='viridis', marker='o')
plt.title('Clusters de Coordenadas com K-means e Número de Ovos')
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# Exibir os centros dos clusters
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], s=200, c='red', marker='x', label='Centros dos Clusters')

plt.legend()
plt.colorbar(scatter, label='Número de Ovos')
plt.show()

# Mostrar o DataFrame com os rótulos de clusters e classificação crítica
print(df)
