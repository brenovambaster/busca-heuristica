import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import para gráficos 3D
from matplotlib.lines import Line2D  # Import para criar uma legenda personalizada

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

# Filtrar os dados para o mês e a semana de referência
df_filtrado = df[(df['Ciclo'] == MES_REFERENCIA) & (df['Semana'] == SEMANA_REFERENCIA)]

# Criar o gráfico 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotar cada ponto com a cor correspondente ao número de ovos
ax.scatter(df_filtrado['Longitude'], df_filtrado['Latitude'], df_filtrado['Ovos'], 
           c=df_filtrado['Cor'], s=50)

# Configurações do gráfico
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Número de Ovos")
ax.set_title(f'Distribuição de armadilhas por quantidade de ovos - {MES_REFERENCIA}/Semana {SEMANA_REFERENCIA}')

# Criar a legenda usando Line2D para representar as cores
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='0-20 Ovos', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='21-40 Ovos', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='41-60 Ovos', markerfacecolor='yellow', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='>60 Ovos', markerfacecolor='red', markersize=10)
]

# Adicionar a legenda ao gráfico
ax.legend(handles=legend_elements, loc="upper right")

# Salvar o gráfico
plt.savefig(f'output/grafico_quantidade_ovos_{MES_REFERENCIA}_sem{SEMANA_REFERENCIA}.png')
plt.show()
