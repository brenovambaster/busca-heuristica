import numpy as np
import pandas as pd
from Individuo import Individuo
from Populacao import Populacao
from processamento import preprocess_data



def main():
    """
    Função principal para executar o pipeline completo do algoritmo genético.
    - Carrega e processa os dados.
    - Inicializa a população.
    - Exibe os indivíduos gerados.
    - Seleciona, recombina e realiza mutação.
    - Identifica o melhor indivíduo.
    """ 

    __TOTAL_GERACAO__ :int = 200

    i =0
    # Carregar e preparar os dados
    data = load_data("data/wine.data")
    features = ['Flavanoids', 'Total_Phenols']
    reduced_data, scaler = preprocess_data(data, features)

    # Criar a população inicial
    populacao = Populacao(tamanho=20, dados=reduced_data)
    
    while i < __TOTAL_GERACAO__:

        # Exibir os indivíduos iniciais
        # exibir_individuos("Indivíduos gerados inicialmente:", populacao.individuos)

        # Selecionar indivíduos para recombinação
        populacao.selecionar_individuos()
        # exibir_individuos("Indivíduos selecionados para recombinação:", populacao.individuos)

        # Realizar recombinação
        populacao.recombinar()
        # exibir_individuos("Indivíduos após recombinação:", populacao.individuos)

        # Aplicar mutação
        populacao.mutar_populacao(dmax=1.0, prob_mutacao=0.03)
        # exibir_individuos("Indivíduos após mutação:", populacao.individuos)

        populacao.substituir_populacao(porcentagem_elite=0.2)

        # Salvar o melhor indivíduo no arquivo saida.out
        with open("saida.out", "a") as f:
            f.write("-" * 60 + "\n")
            f.write("Melhor indivíduo da população:\n")
            if populacao.melhor_global is not None:
                f.write(str(populacao.melhor_global.tolist()) + "\n")
            f.write("-" * 60 + "\n")

        i += 1
    


def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega os dados do arquivo CSV e define os nomes das colunas.

    Parâmetros:
        file_path (str): Caminho do arquivo CSV.

    Retorna:
        pd.DataFrame: Dados carregados com colunas nomeadas.
    """
    columns = [
        'Class', 'Alcohol', 'Malic_Acid', 'Ash', 'Alcalinity_of_Ash',
        'Magnesium', 'Total_Phenols', 'Flavanoids', 'Nonflavanoid_Phenols',
        'Proanthocyanins', 'Color_Intensity', 'Hue',
        'OD280/OD315_of_Diluted_Wines', 'Proline'
    ]
    return pd.read_csv(file_path, names=columns)


def exibir_individuos(titulo: str, individuos: list):
    """
    Exibe os indivíduos formatados no console.

    Parâmetros:
        titulo (str): Título da seção.
        individuos (list): Lista de indivíduos a serem exibidos.
    """
    print_separator()
    print(titulo)
    for ind in individuos:
        print(ind.tolist())
    print_separator()


def print_separator():
    """Imprime um separador visual no console."""
    print("-" * 60)


if __name__ == "__main__":
    main()
