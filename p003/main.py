import pandas as pd
from Populacao import Populacao
from processamento import preprocess_data
from TrocaExtremidadesStrategy import TrocaExtremidadesStrategy
from MediaStrategy import MediaStrategy
import matplotlib.pyplot as plt




def main():
    """
    Função principal para executar o pipeline completo do algoritmo genético.
    - Carrega e processa os dados.
    - Inicializa a população.
    - Exibe os indivíduos gerados.
    - Seleciona, recombina e realiza mutação.
    - Identifica o melhor indivíduo.
    """ 

    __TOTAL_GERACAO__ :int = 500
    __PROB_MUTACAO__ :float = 0.05
    __PORCENTAGEM_ELITE__ :float = 0.23
    __DMAX__ :float = 1.0
    __TAMANHO_POPULACAO__ :int = 20

  
    # Carregar e preparar os dados
    data = load_data("data/wine.data")
    features = ['Flavanoids', 'Total_Phenols']
    reduced_data, scaler = preprocess_data(data, features)

    # Criar a população inicial
    populacao = Populacao(tamanho=__TAMANHO_POPULACAO__, dados=reduced_data)
    
    # Estrarégias para gerar filhos
    troca_extremidades_strategy = TrocaExtremidadesStrategy(data=reduced_data)
    media_strategy = MediaStrategy(data=reduced_data)

    historico = []

    i =0
    while i < __TOTAL_GERACAO__:


        populacao.selecionar_individuos()
        historico.append(populacao.melhor_global.fitness)

        populacao.recombinar(recombinador=media_strategy)
    
        populacao.mutar_populacao(dmax=__DMAX__, prob_mutacao=__PROB_MUTACAO__)

        populacao.substituir_populacao(porcentagem_elite=__PORCENTAGEM_ELITE__)

        # Salvar o melhor indivíduo global no arquivo saida.out
        with open("saida.out", "a") as f:
            f.write("-" * 60 + "\n")
            f.write("Melhor indivíduo da global:\n")
            f.write(str(populacao.melhor_global.tolist()) + "\n")
            f.write("-" * 60 + "\n")

        i += 1
    
    # gerar o gráfico de convergência do melhor indivíduo por geração
    plt.figure(figsize=(10, 6))
    plt.plot(historico, 'b-', label="Fitness do Melhor Indivíduo")
    plt.axhline(y=93.7869, color='r', linestyle='--', label="Saída do KMeans")
    plt.axhline(y=92.2274, color='g', linestyle='--', label="Saída da Busca Local")
    
    plt.title("Convergência do melhor indivíduo por geração. Gerações: " + str(__TOTAL_GERACAO__))
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"convergencia{__TOTAL_GERACAO__}.png")
    plt.show()

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
