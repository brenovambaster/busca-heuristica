

- [1. Busca Local](#1-busca-local)
    - [1.1 Exemplo para ilustrar:](#11-exemplo-para-ilustrar)
  - [1.2 Impacto na Busca Local](#12-impacto-na-busca-local)
- [2. Busca Simultânea ? Implementar se der tempo ?](#2-busca-simultânea--implementar-se-der-tempo-)
- [3. Busca Local e Busca Tabu](#3-busca-local-e-busca-tabu)
  - [3.1 Busca Local](#31-busca-local)
  - [3.2 Busca Tabu](#32-busca-tabu)
- [4. Fatores que Influenciam no Desempenho](#4-fatores-que-influenciam-no-desempenho)
- [5. Cenários Possíveis](#5-cenários-possíveis)
- [6. Exemplo Numérico/Experimental](#6-exemplo-numéricoexperimental)
- [7. Conclusão](#7-conclusão)
- [Melhor solução do Programa já encontrada até então:](#melhor-solução-do-programa-já-encontrada-até-então)


# 1. Busca Local
A busca local, conforme implementada, não explora todas as permutações dos vizinhos. A busca pelo melhor centroide é realizada visitando todos os vizinhos do centróide inicial, e, caso algum desses vizinhos melhore o custo, ele será escolhido. Para cada vizinho, a função de custo é calculada, buscando o menor valor possível.
No entanto, enquanto os vizinhos do centróide do cluster 1 são visitados, os centróides iniciais dos demais clusters permanecem congelados. Isso significa que apenas um centróide é alterado por vez. Para cada centróide i, todos os seus vizinhos são explorados, e o melhor vizinho (aquele que minimiza a função objetivo) é escolhido. Depois de atualizar um centróide, o algoritmo passa para o próximo e repete o processo. Essa abordagem melhora a solução de forma sequencial, centróide por centróide, o que pode levar a um processo de otimização mais lento e suscetível a ficar preso em um mínimo local.
??? Uma outra abordagem seria fazer a permutação (todas as combinações possíveis entre os vizinhos dos 3 centroides, o que levaria uma busca simultânea ou força bruta para analisar todos eles.  ) ????


### 1.1 Exemplo para ilustrar:

Cluster 1: O algoritmo encontra que, ao mover o centróide do cluster 1 para um vizinho, o custo total para o cluster 1 diminui. Isso significa que o centróide foi atualizado para uma melhor posição localmente.

Cluster 2: Quando o algoritmo começa a explorar o cluster 2, ele encontra que movê-lo para um certo vizinho diminui o custo para o cluster 2. Contudo, essa mudança pode aumentar o custo para o cluster 1, pois os dois clusters podem ter centróides muito próximos. Essa proximidade pode alterar a relação entre os pontos e seus centróides nos dois clusters.


## 1.2 Impacto na Busca Local

Atualização Independente: Como o modelo atualiza os centróides independentemente, ele não tem controle global sobre o impacto das mudanças feitas em um cluster sobre os outros. Isso pode levar o modelo a ficar preso em soluções subótimas.

Possibilidade de Mudanças Indesejadas: Uma alteração no centróide do cluster 2 pode aumentar o custo do cluster 1, embora reduza o custo do cluster 2. Essa interdependência entre os clusters não é levada em conta na busca local independente.



# 2. Busca Simultânea ? Implementar se der tempo ?

No modelo ajustado, todos os centróides são avaliados ao mesmo tempo. Para cada centróide, você explora todos os seus vizinhos, mas as mudanças só são aplicadas simultaneamente ao final de cada iteração, em vez de uma por vez.
Se uma melhoria é encontrada em qualquer centróide, ela é aplicada a todos os centróides ao mesmo tempo. O processo continua até que não haja mais melhorias. Essa abordagem ajusta os centróides de forma mais global, permitindo escapar de mínimos locais. No entanto, é mais computacionalmente custosa, pois exige a avaliação de todas as combinações de vizinhos simultaneamente.

2.1 Implicações da Busca Simultânea
Melhor Desempenho Potencial: Avaliando todos os vizinhos ao mesmo tempo, a busca simultânea tem maior potencial de encontrar soluções melhores rapidamente, evitando ficar presa em mínimos locais.


Maior Complexidade Computacional: A busca simultânea é mais cara do ponto de vista computacional, pois exige a avaliação de todos os vizinhos de todos os centróides antes de aplicar uma atualização global.


Maior Risco de Sobrecarga: Quando há muitos centróides e vizinhos, o algoritmo pode enfrentar uma sobrecarga computacional significativa.


Possibilidade de Melhor Resultado: Ao considerar as mudanças de forma global, a busca simultânea pode encontrar soluções melhores do que a busca local independente.



# 3. Busca Local e Busca Tabu

## 3.1 Busca Local

Avalia os vizinhos dos centróides para encontrar configurações melhores. Caso os vizinhos de um centróide atual ofereçam uma redução no custo, a busca local pode escapar de alguns mínimos locais encontrados pelo K-Means. Contudo, a busca local está limitada ao espaço de busca local e pode encontrar apenas um "mínimo local melhor".

## 3.2 Busca Tabu

A busca tabu vai além da busca local ao introduzir uma memória, chamada lista tabu, que evita revisitar soluções exploradas recentemente. Isso permite ao algoritmo explorar mais amplamente o espaço de busca e escapar de mínimos locais.
Critério de Aspiração: Permite ignorar a lista tabu se uma solução tabu oferecer um custo melhor que o melhor já encontrado, aumentando as chances de encontrar o ótimo global.

# 4. Fatores que Influenciam no Desempenho
Vizinhança: A qualidade dos centróides encontrados pela busca local ou tabu depende do design da vizinhança. Um delta (passo) pequeno pode levar a explorações muito restritas, enquanto um delta grande pode tornar a busca ineficaz.


Número de Iterações: Quanto mais iterações forem permitidas, maior será a chance de encontrar soluções melhores.


Parâmetros da Busca Tabu: O tamanho da lista tabu e o critério de aspiração influenciam diretamente no desempenho. Uma lista tabu muito pequena pode levar a ciclos, enquanto uma muito grande pode limitar a exploração.



# 5. Cenários Possíveis
Melhor Solução pelo K-Means: Se o K-Means inicializou os centróides muito perto da solução global, a busca local ou tabu pode não encontrar melhorias significativas.


Melhor Solução pela Busca Local/Tabu: Se o K-Means convergiu para um mínimo local distante do ótimo global, a busca local ou tabu tem grande chance de encontrar melhores configurações de centróides.



# 6. Exemplo Numérico/Experimental
Execução do K-Means: Rode o K-Means e obtenha os centróides iniciais e o custo final. Exemplo: Custo final do K-Means = 1000.5.


Busca Local: Use os centróides encontrados pelo K-Means como ponto de partida e realize a busca local. Exemplo: Após a busca local, o custo foi reduzido para 950.3.


Busca Tabu: Use os centróides do K-Means como ponto de partida, aplique a busca tabu e veja se ela encontra uma solução ainda melhor. Exemplo: Após a busca tabu, o custo foi reduzido para 940.7.



# 7. Conclusão
É possível, e até provável, que a busca local e, principalmente, a busca tabu encontrem soluções melhores do que o K-Means.
O ganho real dependerá da inicialização do K-Means e da eficiência dos parâmetros configurados para as buscas heurísticas.
Experimentos empíricos podem ser realizados para testar os algoritmos no mesmo conjunto de dados, iniciando com os centróides do K-Means como base para as buscas heurísticas.
Visualizar a convergência e os custos históricos ajuda a entender como as soluções evoluem ao longo das iterações.


# Melhor solução do Programa já encontrada até então: 

```shell

Centroides encontrados pelo K-Means: [[ 0.23242425  0.16964401]
 [-1.00234577 -0.99855091]
 [ 1.11694924  1.17118187]]
Custo  total do K-Means: 93.35342525387837
----------------------------------------------------------
Primeiros centr�ides encontrados: [[ 0.43242425  0.26964401]
 [-1.00234577 -0.99855091]
 [ 1.11694924  1.17118187]]
Custo total da busca local primeira melhora: 93.2647516514894
----------------------------------------------------------
Melhores centr�ides encontrados: [[ 0.23242425  0.16964401]
 [-1.00234577 -0.99855091]
 [ 1.01694924  1.07118187]]
Custo total da busca local melhor melhora: 92.74371436432418
----------------------------------------------------------
Itera��o 1: Custo 92.74371436432418
Itera��o 2: Custo 92.39101973947648
Itera��o 3: Custo 92.45105851936727
Itera��o 4: Custo 92.39884176817738
Itera��o 5: Custo 92.46034285168629
Itera��o 6: Custo 92.45978131710984
Itera��o 7: Custo 92.46754231449336
Itera��o 8: Custo 92.72513910309227
Itera��o 9: Custo 92.69947237009191
Itera��o 10: Custo 92.76573887260028
Itera��o 11: Custo 92.62718101838986
Itera��o 12: Custo 92.60403646219089
Itera��o 13: Custo 92.33080378346381
Itera��o 14: Custo 92.22739844004067
Itera��o 15: Custo 92.36611353504297
Itera��o 16: Custo 92.3675815968524
Itera��o 17: Custo 92.41259093865703
Itera��o 18: Custo 92.51492789840214
Itera��o 19: Custo 92.68231177156025
Itera��o 20: Custo 92.33080378346381
Itera��o 21: Custo 92.22739844004067
Itera��o 22: Custo 92.36611353504297
Itera��o 23: Custo 92.3675815968524
Itera��o 24: Custo 92.41259093865703
Itera��o 25: Custo 92.51492789840214
Itera��o 26: Custo 92.68231177156025
Itera��o 27: Custo 92.33080378346381
Itera��o 28: Custo 92.22739844004067
Itera��o 29: Custo 92.36611353504297
Itera��o 30: Custo 92.3675815968524
Itera��o 31: Custo 92.41259093865703
Itera��o 32: Custo 92.51492789840214
Itera��o 33: Custo 92.68231177156025
Itera��o 34: Custo 92.33080378346381
Itera��o 35: Custo 92.22739844004067
Itera��o 36: Custo 92.36611353504297
Itera��o 37: Custo 92.3675815968524
Itera��o 38: Custo 92.41259093865703
Itera��o 39: Custo 92.51492789840214
Itera��o 40: Custo 92.68231177156025
Itera��o 41: Custo 92.33080378346381
Itera��o 42: Custo 92.22739844004067
Itera��o 43: Custo 92.36611353504297
Itera��o 44: Custo 92.3675815968524
Itera��o 45: Custo 92.41259093865703
Itera��o 46: Custo 92.51492789840214
Itera��o 47: Custo 92.68231177156025
Itera��o 48: Custo 92.33080378346381
Itera��o 49: Custo 92.22739844004067
Itera��o 50: Custo 92.36611353504297
Itera��o 51: Custo 92.3675815968524
Itera��o 52: Custo 92.41259093865703
Itera��o 53: Custo 92.51492789840214
Itera��o 54: Custo 92.68231177156025
Itera��o 55: Custo 92.33080378346381
Itera��o 56: Custo 92.22739844004067
Itera��o 57: Custo 92.36611353504297
Itera��o 58: Custo 92.3675815968524
Itera��o 59: Custo 92.41259093865703
Itera��o 60: Custo 92.51492789840214
Itera��o 61: Custo 92.68231177156025
Itera��o 62: Custo 92.33080378346381
Itera��o 63: Custo 92.22739844004067
Itera��o 64: Custo 92.36611353504297
Itera��o 65: Custo 92.3675815968524
Itera��o 66: Custo 92.41259093865703
Itera��o 67: Custo 92.51492789840214
Itera��o 68: Custo 92.68231177156025
Itera��o 69: Custo 92.33080378346381
Itera��o 70: Custo 92.22739844004067
Itera��o 71: Custo 92.36611353504297
Itera��o 72: Custo 92.3675815968524
Itera��o 73: Custo 92.41259093865703
Itera��o 74: Custo 92.51492789840214
Itera��o 75: Custo 92.68231177156025
Itera��o 76: Custo 92.33080378346381
Itera��o 77: Custo 92.22739844004067
Itera��o 78: Custo 92.36611353504297
Itera��o 79: Custo 92.3675815968524
Itera��o 80: Custo 92.41259093865703
Itera��o 81: Custo 92.51492789840214
Itera��o 82: Custo 92.68231177156025
Itera��o 83: Custo 92.33080378346381
Itera��o 84: Custo 92.22739844004067
Itera��o 85: Custo 92.36611353504297
Itera��o 86: Custo 92.3675815968524
Itera��o 87: Custo 92.41259093865703
Itera��o 88: Custo 92.51492789840214
Itera��o 89: Custo 92.68231177156025
Itera��o 90: Custo 92.33080378346381
Itera��o 91: Custo 92.22739844004067
Itera��o 92: Custo 92.36611353504297
Itera��o 93: Custo 92.3675815968524
Itera��o 94: Custo 92.41259093865703
Itera��o 95: Custo 92.51492789840214
Itera��o 96: Custo 92.68231177156025
Itera��o 97: Custo 92.33080378346381
Itera��o 98: Custo 92.22739844004067
Itera��o 99: Custo 92.36611353504297
Itera��o 100: Custo 92.3675815968524
Itera��o 101: Custo 92.41259093865703
Itera��o 102: Custo 92.51492789840214
Itera��o 103: Custo 92.68231177156025
Itera��o 104: Custo 92.33080378346381
Itera��o 105: Custo 92.22739844004067
Itera��o 106: Custo 92.36611353504297
Itera��o 107: Custo 92.3675815968524
Itera��o 108: Custo 92.41259093865703
Itera��o 109: Custo 92.51492789840214
Itera��o 110: Custo 92.68231177156025
Itera��o 111: Custo 92.33080378346381
Itera��o 112: Custo 92.22739844004067
Itera��o 113: Custo 92.36611353504297
Itera��o 114: Custo 92.3675815968524
Itera��o 115: Custo 92.41259093865703
Itera��o 116: Custo 92.51492789840214
Itera��o 117: Custo 92.68231177156025
Itera��o 118: Custo 92.33080378346381
Itera��o 119: Custo 92.22739844004067
Itera��o 120: Custo 92.36611353504297
Itera��o 121: Custo 92.3675815968524
Itera��o 122: Custo 92.41259093865703
Itera��o 123: Custo 92.51492789840214
Itera��o 124: Custo 92.68231177156025
Itera��o 125: Custo 92.33080378346381
Itera��o 126: Custo 92.22739844004067
Itera��o 127: Custo 92.36611353504297
Itera��o 128: Custo 92.3675815968524
Itera��o 129: Custo 92.41259093865703
Itera��o 130: Custo 92.51492789840214
Itera��o 131: Custo 92.68231177156025
Itera��o 132: Custo 92.33080378346381
Itera��o 133: Custo 92.22739844004067
Itera��o 134: Custo 92.36611353504297
Itera��o 135: Custo 92.3675815968524
Itera��o 136: Custo 92.41259093865703
Itera��o 137: Custo 92.51492789840214
Itera��o 138: Custo 92.68231177156025
Itera��o 139: Custo 92.33080378346381
Itera��o 140: Custo 92.22739844004067
Itera��o 141: Custo 92.36611353504297
Itera��o 142: Custo 92.3675815968524
Itera��o 143: Custo 92.41259093865703
Itera��o 144: Custo 92.51492789840214
Itera��o 145: Custo 92.68231177156025
Itera��o 146: Custo 92.33080378346381
Itera��o 147: Custo 92.22739844004067
Itera��o 148: Custo 92.36611353504297
Itera��o 149: Custo 92.3675815968524
Itera��o 150: Custo 92.41259093865703
Melhores centr�ides pela busca tabu: [[ 0.13242425 -0.03035599]
 [-1.20234577 -1.09855091]
 [ 1.01694924  0.97118187]]
Custo final da busca tabu: 92.22739844004067
----------------------------------------------------------
											
```