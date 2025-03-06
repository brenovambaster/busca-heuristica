from pydoc import doc
from typing import Tuple, ClassVar
import numpy as np
from Individuo import Individuo

class Recombinador:
    """
    Classe responsável pelas operações de recombinação (crossover) entre indivíduos.
    
    Esta classe implementa diferentes estratégias de recombinação genética para
    gerar novos indivíduos a partir de pais selecionados, facilitando a exploração
    do espaço de soluções no algoritmo genético aplicado ao k-means.
    
    Attributes:
        dados (ClassVar[np.ndarray]): Conjunto de dados compartilhado usado para calcular
                                     o fitness dos novos indivíduos gerados.
    """
    
    # Atributo estático para armazenar os dados compartilhados por todos os indivíduos
    dados: ClassVar[np.ndarray]

    def __init__(self,data: np.ndarray) -> None:
        """
        Inicializa a classe Recombinador com os dados compartilhados.
        
        Args:
            data: Conjunto de dados no formato (n_samples, n_features), onde cada
                 linha representa um ponto com coordenadas (x, y).
        """
        Recombinador.set_dados(data)
        

    @classmethod
    def set_dados(cls, dados: np.ndarray) -> None:
        """
        Define o conjunto de dados compartilhado usado para calcular o fitness.
        
        Args:
            dados: Conjunto de dados no formato (n_samples, n_features), onde cada
                 linha representa um ponto com coordenadas (x, y).
        """
        cls.dados = dados

    @classmethod
    def recombinar_troca_extremidades(cls, ind1: Individuo, ind2: Individuo) -> Tuple[Individuo, Individuo]:
        """
        Realiza recombinação por troca de extremidades entre dois indivíduos.
        
        Implementa uma estratégia de recombinação onde os centróides das extremidades
        são trocados entre os pais, enquanto o centróide central de cada pai é mantido.
        Isso promove a diversidade da população enquanto preserva parte da estrutura de
        cada solução parental.
        
        Esquema de recombinação:
            - Filho 1: [centróide esquerdo do ind2, centróide central do ind1, centróide direito do ind2]
            - Filho 2: [centróide esquerdo do ind1, centróide central do ind2, centróide direito do ind1]
        
        Args:
            ind1: Primeiro indivíduo pai.
            ind2: Segundo indivíduo pai.
        
        Returns:
            Um par contendo dois novos indivíduos filhos resultantes da recombinação.
        
        Raises:
            ValueError: Se o atributo dados não tiver sido inicializado.
        """
        if cls.dados is None:
            raise ValueError("É necessário definir os dados com set_dados() antes de recombinar indivíduos")
            
        # Cópia dos centróides para evitar efeitos colaterais
        centroide_esquerda_i1 = ind1.individuo[0].copy()
        centroide_central_i1 = ind1.individuo[1].copy()
        centroide_direita_i1 = ind1.individuo[2].copy()

        centroide_esquerda_i2 = ind2.individuo[0].copy()
        centroide_central_i2 = ind2.individuo[1].copy()
        centroide_direita_i2 = ind2.individuo[2].copy()

        # Cria os filhos
        filho1 = Individuo(data=cls.dados)
        filho2 = Individuo(data=cls.dados)

        # Filho 1: usa a extremidade esquerda de ind2, centróide central de ind1 e extremidade direita de ind2
        

        filho1.individuo[0] = centroide_esquerda_i2
        filho1.individuo[1] = centroide_central_i1
        filho1.individuo[2] = centroide_direita_i2

        # Filho 2: usa a extremidade esquerda de ind1, centróide central de ind2 e extremidade direita de ind1
        filho2.individuo[0] = centroide_esquerda_i1
        filho2.individuo[1] = centroide_central_i2
        filho2.individuo[2] = centroide_direita_i1

        filho1.calculate_fitness(cls.dados)
        filho2.calculate_fitness(cls.dados)

        return filho1, filho2

    @classmethod
    def recombinar_media(cls, ind1: Individuo, ind2: Individuo) -> Individuo:
        """
        Realiza recombinação por média aritmética das coordenadas dos pais.
        
        Esta estratégia gera um único filho cujas coordenadas de cada centróide
        são a média aritmética das coordenadas correspondentes dos pais. Este método
        tende a produzir soluções que combinam características de ambos os pais,
        favorecendo a exploração do espaço intermediário entre soluções promissoras.
        
        Esquema de recombinação:
            - Para cada centróide i:
              Filho[i] = (ind1[i] + ind2[i]) / 2
        
        Args:
            ind1: Primeiro indivíduo pai.
            ind2: Segundo indivíduo pai.
        
        Returns:
            Um novo indivíduo filho gerado pela média das coordenadas.
            
        Raises:
            ValueError: Se o atributo dados não tiver sido inicializado.
        """
        if cls.dados is None:
            raise ValueError("É necessário definir os dados com set_dados() antes de recombinar indivíduos")
            
        media_centroide_esquerda = (ind1.individuo[0] + ind2.individuo[0]) / 2
        media_centroide_meio = (ind1.individuo[1] + ind2.individuo[1]) / 2
        media_centroide_direita = (ind1.individuo[2] + ind2.individuo[2]) / 2

        filho = Individuo(data=cls.dados)
        filho.individuo[0] = media_centroide_esquerda
        filho.individuo[1] = media_centroide_meio
        filho.individuo[2] = media_centroide_direita

        return filho