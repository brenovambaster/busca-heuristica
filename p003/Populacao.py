
import copy
from traceback import print_tb
import numpy as np
from typing import List, Optional
from Individuo import Individuo
from RecombinadorStrategy import RecombinadorStrategy
import random

class Populacao:
    """
    Classe que gerencia uma população de indivíduos para um algoritmo genético.
    
    Esta classe implementa os mecanismos de evolução para otimização baseada em algoritmos
    genéticos, incluindo inicialização, seleção, recombinação, mutação e substituição
    de indivíduos em cada geração.
    
    Attributes:
        tamanho (int): Número de indivíduos na população.
        dados (np.ndarray): Base de dados utilizada para o cálculo do fitness.
        individuos (List[Individuo]): Lista contendo os indivíduos da população atual.
        melhor_global (Individuo]: Melhor indivíduo encontrado até o momento.
    """


    def __init__(self, tamanho: int, dados: np.ndarray) -> None:
        """
        Inicializa a população com o número especificado de indivíduos.
        
        Args:
            tamanho: Número de indivíduos na população.
            dados: Base de dados a ser utilizada para o cálculo do fitness.
        """

        self.tamanho = tamanho
        self.dados = dados
        self.individuos: List[Individuo] = self._inicializar_populacao()
        self.individuos.sort(key=lambda ind: ind.fitness)
        self.melhor_global = copy.deepcopy(self.individuos[0])

    def _inicializar_populacao(self) -> List[Individuo]:
        """
        Cria a população inicial com indivíduos configurados.
        
        Inicializa a população incorporando soluções anteriores, se disponíveis,
        e preenche o restante com indivíduos aleatórios até atingir o tamanho
        especificado da população.
        
        Returns:
            Lista de indivíduos que compõem a população inicial.
        """
        populacao: List[Individuo] = []
       
        solucao_anterior: List[Individuo] = self._obter_solucao_anterior()
        populacao.extend(solucao_anterior)

        # Preenche o restante de indivíduos com centróides aleatórios
        while len(populacao) < self.tamanho:
            centros = self._gerar_centroide_aleatorio()
            individuo = Individuo(data=self.dados, individuo=centros)
            populacao.append(individuo)
        
        return populacao

    def _gerar_centroide_aleatorio(self) -> np.ndarray:
        """
        Gera centróides aleatórios para inicialização de indivíduos.
        
        Cria um conjunto de 3 centróides aleatórios distribuídos uniformemente
        no espaço de busca bidimensional.
        
        Returns:
            Array de centróides com formato (3, 1, 2), onde cada centróide
            é representado por coordenadas (x, y).
        """
        centros = []
        for _ in range(3):
            # Aqui definimos os limites do espaço (exemplo: entre 0 e 2)
            x = np.random.uniform(0, 2)
            y = np.random.uniform(0, 2)
            centros.append([[x, y]])
        return np.array(centros)

    def _obter_solucao_anterior(self) -> List[Individuo]:
        """
        Recupera soluções anteriores para inicializar parte da população.

        Permite reutilizar soluções obtidas por outros métodos (como busca
        construtiva ou busca tabu) para inicializar parte da população,
        aproveitando conhecimento prévio do espaço de busca.
        
        Returns:
            Lista de indivíduos baseados em soluções anteriores.
        """
        solucao_busca_construtiva = [
            [0.23242425, 0.16964401], 
            [-1.00234577, -0.99855091], 
            [1.11694924, 1.17118187]
        ]
        solucao_busca_construtiva = np.array(solucao_busca_construtiva)

        return [Individuo(data=self.dados, individuo=solucao_busca_construtiva)]


    
    def _set_melhor_individuo_global(self) -> None:
        """
        Atualiza o melhor indivíduo global com base no melhor indivíduo atual.
        """
        self.individuos.sort(key=lambda ind: ind.fitness)
        melhor_atual = copy.deepcopy(self.individuos[0])
        

        if melhor_atual.fitness < self.melhor_global.fitness: 
            self.melhor_global = copy.deepcopy(melhor_atual) 

            
    def selecionar_individuos(self) -> List[Individuo]:
        """
        Seleciona indivíduos para recombinação.
        
        Implementa uma estratégia de seleção ordenando os indivíduos pelo fitness,
        priorizando os melhores indivíduos para a recombinação.
        
        Returns:
            Lista de indivíduos selecionados para recombinação, ordenados por fitness.
        """
        # Ordena os indivíduos atuais pela qualidade (fitness)
        # Assim, ao gerar os filhos, sempre vão pegar os melhores pais primeiro
        self.individuos.sort(key=lambda ind: ind.fitness)
        return self.individuos

    def recombinar(self, recombinador:RecombinadorStrategy) -> List[Individuo]:
        """
        Realiza a recombinação genética entre indivíduos para gerar novos indivíduos.
        
        Utiliza o método de recombinação por troca de extremidades, aplicado a pares
        consecutivos de indivíduos selecionados.

        Args:
            recombinador: Estratégia de recombinação a ser utilizada.
        
        Returns:
            Lista dos novos indivíduos (filhos) gerados pela recombinação.
        """
        novos_individuos = []
        
        pais = self.selecionar_individuos()
    
        for i in range(0, len(pais) - 1, 2):
            filhos = recombinador.recombinar(pais[i], pais[i+1])
            
            # Se o recombinação retornar apenas um filho, converte para lista
            if not isinstance(filhos, (list)):
                filhos = [filhos]
            
            novos_individuos.extend(filhos)
    
        self.individuos.extend(novos_individuos)
        self._set_melhor_individuo_global()
        return self.individuos

    def mutar_populacao(self,*,dmax: float=1, prob_mutacao: float = 0.03) -> None:
        """
        Aplica operador de mutação a todos os indivíduos da população.
        
        A mutação permite explorar novas regiões do espaço de busca,
        alterando aleatoriamente as características dos indivíduos.
        
        Args:
            dmax: Valor máximo de alteração para cada coordenada durante a mutação.
            prob_mutacao: Probabilidade de mutação para cada coordenada (default: 0.03).
        """
        for individuo in self.individuos:
            individuo.mutate(dmax, prob_mutacao)

        self._set_melhor_individuo_global()
       

    def substituir_populacao(self, porcentagem_elite: float = 0.2) -> None:
        """
        Substitui a população atual por uma nova geração de indivíduos.
        
        Preserva a elite e realiza seleção proporcional ao fitness para os demais.
        
        Args:
            porcentagem_elite: Proporção dos melhores indivíduos a serem preservados.
        """
        
        
        self.individuos.sort(key=lambda ind: ind.fitness)

        qtd_elite = int(self.tamanho * porcentagem_elite)
        elite = self.individuos[:qtd_elite]

        # Verificar se há alguém na elite com fitness igual ou melhor que o melhor global
        melhor_global_representado = any(ind.fitness <= self.melhor_global.fitness for ind in elite)

        if not melhor_global_representado:
            # print("Melhor global não está representado na elite")
            # Substituir o pior membro da elite (considerando que elite já está ordenada)
            elite[-1] = self.melhor_global

        restantes = self.individuos[qtd_elite:]

       
        """
            indivíduos com fitness menor terão um peso maior (pois 1.0 f/ fitness aumenta quando fitness diminui).
            Isso garante que indivíduos com fitness menor tenham uma chance maior de serem selecionados.
        """
        pesos = [(1.0 / ind.fitness if ind.fitness > 0 else 1.0) for ind in restantes]

        qtd_restante = self.tamanho - len(elite)
        selecionados = random.choices(restantes, weights=pesos, k=qtd_restante)

        
        self.individuos = elite + selecionados
        self._set_melhor_individuo_global()
