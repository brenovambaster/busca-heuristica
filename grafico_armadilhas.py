import pandas as pd
import matplotlib.pyplot as plt

# Configurações
MES_REFERENCIA = 'Janeiro'

# Carregar o arquivo CSV com delimitador ';'
df = pd.read_csv('data/data.csv', delimiter=';')

# Substituir vírgulas por pontos nas colunas de Latitude e Longitude e converter para float
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Determinar a cor com base na quantidade de ovos
def get_color(ovos):
    if 0 <= ovos <= 9:
        return 'green'
    elif 10 <= ovos <= 40:
        return 'orange'
    elif ovos > 40:
        return 'red'


# Adicionar uma coluna 'Cor' no DataFrame com base na quantidade de ovos
df['Cor'] = df['Ovos'].apply(get_color)

# Criar o gráfico 2D com latitude e longitude
plt.figure(figsize=(10, 8))

# Loop para plotar os pontos até encontrar um ciclo diferente de "Janeiro"
for idx, row in df.iterrows():  
    if row['Ciclo'] != 'Janeiro':
        break  # Parar o loop se o ciclo não for 'Janeiro'
    
    plt.scatter(row['Longitude'], row['Latitude'], color=row['Cor'], s=50)

# Configurações do gráfico
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Distribuição de armadilhas e quantidades de ovos Espaço 2D - "+ MES_REFERENCIA)
plt.grid(True)

# Criar a legenda com pontos de exemplo para representar as cores
plt.scatter([], [], color='green', label='0-5 ovos')
plt.scatter([], [], color='orange', label='10-40 ovos')
plt.scatter([], [], color='red', label='>40 ovos')

# Adicionar a legenda ao gráfico
plt.legend(loc="upper right")

# Exibir o gráfico
plt.savefig("output/grafico_armadilhas.png")
plt.show()
