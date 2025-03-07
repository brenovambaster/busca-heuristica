from abc import ABC, abstractmethod
from typing import Tuple, Union
import numpy as np
from Individuo import Individuo
from typing import Tuple, ClassVar
from RecombinadorStrategy import RecombinadorStrategy

class TrocaExtremidadesStrategy(RecombinadorStrategy):
    """
    Classe responsável pela recombinação de indivíduos por troca de extremidades.
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
    
    def recombinar(self, ind1: Individuo, ind2: Individuo) -> list[Individuo]:
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
        
        if self.dados is None:
            raise ValueError("É necessário definir os dados com set_dados() antes de recombinar indivíduos")
           
        # Cópia dos centróides
        centroide_esquerda_i1 = ind1.individuo[0].copy()
        centroide_central_i1  = ind1.individuo[1].copy()
        centroide_direita_i1  = ind1.individuo[2].copy()
        centroide_esquerda_i2 = ind2.individuo[0].copy()
        centroide_central_i2  = ind2.individuo[1].copy()
        centroide_direita_i2  = ind2.individuo[2].copy()

        filho1 = Individuo(data=self.dados)
        filho2 = Individuo(data=self.dados)
        
        filho1.individuo[0] = centroide_esquerda_i2
        filho1.individuo[1] = centroide_central_i1
        filho1.individuo[2] = centroide_direita_i2

        filho2.individuo[0] = centroide_esquerda_i1
        filho2.individuo[1] = centroide_central_i2
        filho2.individuo[2] = centroide_direita_i1

        filho1.calculate_fitness(self.dados)
        filho2.calculate_fitness(self.dados)
        return [filho1, filho2]
