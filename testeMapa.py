import pandas as pd
import folium

# Configurações
MES_REFERENCIA = 'Janeiro'
SEMANA_REFERENCIA = 3

# Carregar o arquivo CSV com delimitador ';'
df = pd.read_csv(f'data/data_{MES_REFERENCIA}.csv', delimiter=';')

# Substituir vírgulas por pontos nas colunas de Latitude e Longitude e converter para float
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Determinar a cor com base na quantidade de ovos, usando as cores válidas de folium.Icon
def get_color(ovos):
    if 0 <= ovos <= 50:
        return 'green'        # Baixo risco
    elif 51 <= ovos <= 100:
        return 'lightgreen'   # Risco moderado
    elif 101 <= ovos <= 150:
        return 'orange'       # Risco alto
    elif 151 <= ovos <= 200:
        return 'red'          # Risco muito alto
    elif 201 <= ovos <= 250:
        return 'purple'       # Emergência
    elif 251 <= ovos <= 300:
        return 'darkpurple'   # Emergência extrema
    elif ovos > 300:
        return 'black'        # Risco máximo

# Adicionar uma coluna 'Cor' no DataFrame com base na quantidade de ovos
df['Cor'] = df['Ovos'].apply(get_color)

# Inicializar o mapa com o estilo satélite
mapa = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Adicionar marcadores padrão no mapa
for idx, row in df.iterrows():  
    if row['Ciclo'] == MES_REFERENCIA and row['Semana'] == SEMANA_REFERENCIA:
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.Icon(color=row['Cor'], icon="info-sign"),
            popup=folium.Popup(f"Ovos: {row['Ovos']}<br>Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}", max_width=250)
        ).add_to(mapa)

# Salvar o mapa como um arquivo HTML
mapa.save(f'output/mapa_armadilhas_{MES_REFERENCIA}_sem{SEMANA_REFERENCIA}.html')
