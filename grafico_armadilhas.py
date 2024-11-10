import pandas as pd
import matplotlib.pyplot as plt

# Configurações
MES_REFERENCIA = 'Março'
SEMANA_REFERENCIA = 13


# Carregar o arquivo CSV com delimitador ';'
df = pd.read_csv(f'data/data_{MES_REFERENCIA}.csv', delimiter=';')

# Substituir vírgulas por pontos nas colunas de Latitude e Longitude e converter para float
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Determinar a cor com base na quantidade de ovos
def get_color(ovos):
    if 0 <= ovos <= 50:
        return 'green'  # Baixo risco
    elif 51 <= ovos <= 100:
        return 'yellow'  # Risco moderado
    elif 101 <= ovos <= 150:
        return 'orange'  # Risco alto
    elif 151 <= ovos <= 200:
        return 'red'  # Risco muito alto
    elif 201 <= ovos <= 250:
        return 'purple'  # Emergência
    elif 251 <= ovos <= 300:
        return 'blue'  # Emergência extrema
    elif ovos > 300:
        return 'darkviolet'

# Adicionar uma coluna 'Cor' no DataFrame com base na quantidade de ovos
df['Cor'] = df['Ovos'].apply(get_color)

# Criar o gráfico 2D com latitude e longitude
plt.figure(figsize=(10, 8))

# Loop para plotar os pontos até encontrar um ciclo diferente de "Janeiro"
for idx, row in df.iterrows():  
    if row['Ciclo'] == MES_REFERENCIA and row['Semana'] == SEMANA_REFERENCIA:
        plt.scatter(row['Longitude'], row['Latitude'], color=row['Cor'], s=50)


# Configurações do gráfico
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f'Distribuição de armadilhas e quantidades de ovos Espaço 2D -{MES_REFERENCIA}/Semana {SEMANA_REFERENCIA}')
plt.grid(True)

# Criar a legenda com pontos de exemplo para representar as cores
plt.scatter([], [], color='green', label='0-50 ovos')
plt.scatter([], [], color='yellow', label='51-100 ovos')
plt.scatter([], [], color='orange', label='101-150 ovos')
plt.scatter([], [], color='red', label='151-200 ovos')
plt.scatter([], [], color='purple', label='201-250 ovos')
plt.scatter([], [], color='blue', label='251-300 ovos')
plt.scatter([], [], color='darkviolet', label='>300 ovos')
plt.legend(title='Quantidade de ovos', loc="upper right")

# Exibir o gráfico
plt.savefig(f'output/grafico_armadilhas_{MES_REFERENCIA}_sem{SEMANA_REFERENCIA}.png')
plt.show()
