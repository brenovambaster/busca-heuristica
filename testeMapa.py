import pandas as pd
import folium

# Carregar o arquivo CSV com delimitador ';'
df = pd.read_csv('data/data.csv', delimiter=';')

# Substituir vírgulas por pontos nas colunas de Latitude e Longitude e converter para float
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Criar o mapa centrado em um ponto inicial (coordenadas médias da área de interesse)
mapa = folium.Map(location=[-16.725469, -43.8476385], zoom_start=10)

# Adicionar marcadores para cada ponto de latitude e longitude, com cores baseadas na quantidade de ovos
for idx, row in df.iterrows():
    # Determinar a cor do marcador com base na quantidade de ovos
    if 0 <= row['Ovos'] <= 5:
        color = 'green'
    elif 10 <= row['Ovos'] <= 40:
        color = 'orange'
    elif row['Ovos'] > 40:
        color = 'red'
    else:
        color = 'blue'  # Cor padrão para valores fora dos intervalos definidos, caso necessário

    # Criar o conteúdo do popup
    popup_content = f"""
    <b>Cidade:</b> {row['Município']}<br>
    <b>Resultado:</b> {row['Resultado']}<br>
    <b>Ciclo:</b> {row['Ciclo']}<br>
    <b>Ovos:</b> {row['Ovos']}
    """
    popup = folium.Popup(popup_content, max_width=300)  # Define a largura do popup

    # Adicionar o marcador ao mapa com o popup ajustado
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup,
        icon=folium.Icon(color=color)
    ).add_to(mapa)
    
    # Interrompe o loop se o ciclo não for 'Janeiro' (se necessário para depuração)
    if row['Ciclo'] != 'Janeiro':
        break

# Salvar o mapa em um arquivo HTML
mapa.save("mapa_dengue.html")
mapa
