from re import S
from tkinter.messagebox import RETRY
import numpy as np
from typing import List, Optional, Union
from Individuo import Individuo
from Recombinador import Recombinador
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
        melhor_global (Optional[Individuo]): Melhor indivíduo encontrado até o momento.
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
        self.melhor_global = self.individuos[0]

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
        if solucao_anterior is not None:
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

    def _melhor_individuo_atual(self) -> Optional[Individuo]:
        """
        Identifica e armazena o melhor indivíduo da população atual.
        
        Ordena os indivíduos pelo fitness e atualiza o melhor indivíduo global
        se um novo melhor for encontrado.
        
        Returns:
            O melhor indivíduo da população atual ou None se a população estiver vazia.
        """
        
        self.individuos.sort(key=lambda ind: ind.fitness)

        return self.individuos[0]
    
    def _set_melhor_individuo_global(self) -> None:
        """
        Atualiza o melhor indivíduo global com base no melhor indivíduo atual.
        """
        melhor_atual = self._melhor_individuo_atual()
        
        if melhor_atual is not None:  # Certifica-se de que há um melhor indivíduo
            if  melhor_atual.fitness < self.melhor_global.fitness:
                self.melhor_global = melhor_atual  # Garante que o melhor global é sempre atualizado

            
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
        self._melhor_individuo_atual()

        return self.individuos

    def recombinar(self) -> List[Individuo]:
        """
        Realiza a recombinação genética entre indivíduos para gerar novos indivíduos.
        
        Utiliza o método de recombinação por troca de extremidades, aplicado a pares
        consecutivos de indivíduos selecionados.
        
        Returns:
            Lista dos novos indivíduos (filhos) gerados pela recombinação.
        """
        novos_individuos = []
        Recombinador.set_dados(self.dados)
        pais = self.selecionar_individuos()
    
        for i in range(0, len(pais) - 1, 2):
            filho1, filho2 = Recombinador.recombinar_troca_extremidades(pais[i], pais[i+1])
            # OUTRA FORMA SERIA: filho1 = Recombinador.recombinar_media(pais[i], pais[i+1])
            novos_individuos.extend([filho1, filho2])
    
        self.individuos.extend(novos_individuos)
        self._set_melhor_individuo_global()

        return self.individuos

    def mutar_populacao(self,*,dmax: float, prob_mutacao: float = 0.03) -> None:
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

        # Mantém o melhor global manualmente
        if self.melhor_global not in elite:
            elite.append(self.melhor_global)

        restantes = self.individuos[qtd_elite:]
        pesos = [(1.0 / ind.fitness if ind.fitness > 0 else 1.0) for ind in restantes]

        qtd_restante = self.tamanho - len(elite)
        selecionados = random.choices(restantes, weights=pesos, k=qtd_restante)

        self.individuos = elite + selecionados

        # Atualiza o melhor global para garantir que ele não seja perdido
        self._set_melhor_individuo_global()

    def proxima_geracao(self, dmax: float, prob_mutacao: float = 0.03, porcentagem_elite: float = 0.2) -> None:
        """
        Evolui a população para a próxima geração.
        
        Executa o ciclo completo de um algoritmo genético:
        1. Recombinação: gera novos indivíduos (filhos)
        2. Mutação: aplica operador de mutação aos filhos
        3. Substituição: forma a nova geração combinando elite e indivíduos selecionados
        
        Args:
            dmax: Valor máximo de alteração para cada coordenada durante a mutação.
            prob_mutacao: Probabilidade de mutação para cada coordenada (default: 0.03).
            porcentagem_elite: Proporção dos melhores indivíduos a serem preservados (default: 0.2).
        """
        # Recombina os indivíduos para gerar filhos
        self.recombinar()
        
        # NÃO NECESSARIAMENTE APLICA-SE PARA TODOS OS FILHOS
        # Aplica mutação a todos os filhos 
        # for individuo in filhos:
        #     individuo.mutate(dmax, prob_mutacao)
            
        # Realiza a substituição para formar a nova geração
        self.substituir_populacao(porcentagem_elite)