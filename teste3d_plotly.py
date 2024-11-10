import pandas as pd
import plotly.graph_objects as go

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
        return 'darkviolet'  # Máxima emergência

# Adicionar uma coluna 'Cor' no DataFrame com base na quantidade de ovos
df['Cor'] = df['Ovos'].apply(get_color)

# Filtrar os dados para o mês e a semana de referência
df_filtrado = df[(df['Ciclo'] == MES_REFERENCIA) & (df['Semana'] == SEMANA_REFERENCIA)]

# Criar o gráfico 3D usando Plotly
fig = go.Figure()

# Adicionar os pontos ao gráfico 3D para cada faixa de ovos
for ovos_min, ovos_max, cor, label in [
    (0, 50, 'green', '0-50 ovos (Baixo risco)'),
    (51, 100, 'yellow', '51-100 ovos (Risco moderado)'),
    (101, 150, 'orange', '101-150 ovos (Risco alto)'),
    (151, 200, 'red', '151-200 ovos (Risco muito alto)'),
    (201, 250, 'purple', '201-250 ovos (Emergência)'),
    (251, 300, 'blue', '251-300 ovos (Emergência extrema)'),
    (301, float('inf'), 'darkviolet', '>300 ovos (Máxima emergência)')
]:
    subset = df_filtrado[(df_filtrado['Ovos'] >= ovos_min) & (df_filtrado['Ovos'] <= ovos_max)]
    
    fig.add_trace(go.Scatter3d(
        x=subset['Longitude'],
        y=subset['Latitude'],
        z=subset['Ovos'],
        mode='markers',
        marker=dict(
            size=5,
            color=cor,  # Atribuir a cor correspondente ao intervalo de ovos
            opacity=0.8
        ),
        name=label  # Nome para a legenda
    ))

# Configurações do layout do gráfico
fig.update_layout(
    scene=dict(
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        zaxis_title="Número de Ovos"
    ),
    title=f'Distribuição de armadilhas por quantidade de ovos - {MES_REFERENCIA}/Semana {SEMANA_REFERENCIA}',
    margin=dict(l=0, r=0, b=0, t=40)
)
# Exibir o gráfico interativo
fig.show()
