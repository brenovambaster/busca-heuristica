from RecombinadorStrategy import RecombinadorStrategy
from Individuo import Individuo
from typing import ClassVar
import numpy as np




class MediaStrategy(RecombinadorStrategy):
    """
    Classe que implementa a estratégia de recombinação baseada na média dos centróides.
    """
    # Atributo estático para armazenar os dados compartilhados por todos os indivíduos
    dados: ClassVar[np.ndarray]

    @classmethod
    def __init__(cls,data: np.ndarray) -> None:
        """
        Inicializa a classe Recombinador com os dados compartilhados.
        
        Args:
            data: Conjunto de dados no formato (n_samples, n_features), onde cada
                 linha representa um ponto com coordenadas (x, y).
        """
        cls.dados = data
    
    def recombinar(self, ind1: Individuo, ind2: Individuo) -> Individuo:
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
        if self.dados is None:
            raise ValueError("É necessário definir os dados com set_dados() antes de recombinar indivíduos")
           
        media_centroide_esquerda = (ind1.individuo[0] + ind2.individuo[0]) / 2
        media_centroide_meio     = (ind1.individuo[1] + ind2.individuo[1]) / 2
        media_centroide_direita  = (ind1.individuo[2] + ind2.individuo[2]) / 2

        filho = Individuo(data=self.dados)
        filho.individuo[0] = media_centroide_esquerda
        filho.individuo[1] = media_centroide_meio
        filho.individuo[2] = media_centroide_direita

        filho.calculate_fitness(self.dados)
        return filho