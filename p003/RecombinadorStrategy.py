from abc import ABC, abstractmethod
from typing import Tuple, Union
import numpy as np
from Individuo import Individuo
from typing import ClassVar

class RecombinadorStrategy(ABC):
    """
    Classe abstrata que define a interface para as estratégias de recombinação de indivíduos.
    """

    @abstractmethod
    def __init__(cls,data: np.ndarray) -> None:
        """
        Inicializa a classe Recombinador com os dados compartilhados.
        
        Args:
            data: Conjunto de dados no formato (n_samples, n_features), onde cada
                 linha representa um ponto com coordenadas (x, y).
        """
        pass

    @abstractmethod
    def recombinar(cls, ind1: Individuo, ind2: Individuo) -> list[Individuo]| Individuo:
        """
        Realiza a recombinação entre dois indivíduos, gerando um ou dois novos indivíduos.
        """
        pass
