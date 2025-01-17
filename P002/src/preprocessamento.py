import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def preprocess_data(data: pd.DataFrame, features: list):
    """
    Prepara os dados para análise, selecionando características específicas e normalizando.

    Args:
        data (pd.DataFrame): Dados de entrada no formato de DataFrame.
        features (list): Lista de nomes das colunas a serem usadas.

    Returns:
        tuple: Dados normalizados (np.ndarray) e o objeto scaler usado para normalização.
    """
    # Seleciona as características escolhidas pelo usuário
    reduced_data = data[features]

    # Normaliza os dados usando o StandardScaler
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(reduced_data)

    return normalized_data, scaler
