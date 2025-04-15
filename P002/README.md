- [📌 Descrição do Projeto](#-descrição-do-projeto)
- [Documentos](#documentos)
  - [🧪 Técnicas Implementadas](#-técnicas-implementadas)
    - [🔍 Busca Local](#-busca-local)
    - [🔍 Busca Tabu](#-busca-tabu)
  - [📊 Vizinhanças](#-vizinhanças)
  - [Fatores que Influenciam o Desempenho](#fatores-que-influenciam-o-desempenho)
  - [Cenários Possíveis](#cenários-possíveis)
  - [Exemplo Numérico/Experimental](#exemplo-numéricoexperimental)
  - [📈 Exemplos de Resultados](#-exemplos-de-resultados)
  - [Conclusão](#conclusão)
  - [👥 Autores](#-autores)
  - [Resultados Obtidos](#resultados-obtidos)

# 📌 Descrição do Projeto

Este projeto foi desenvolvido para a disciplina de Técnicas de Busca Heurística do curso de Ciência da Computação do IFNMG. Ele explora o uso de técnicas de busca local (primeira melhora e melhor melhora) e busca tabu para otimizar o problema de agrupamento baseado em centróides, inicialmente resolvido pelo algoritmo K-Means.

A base de dados Wine foi utilizada, reduzida a duas dimensões (R²) com os atributos Flavonoides e Fenóis Totais. O objetivo é minimizar o somatório das distâncias euclidianas dos registros aos seus respectivos centróides, empregando técnicas de vizinhança para explorar diferentes configurações de centróides e aprimorar as soluções do K-Means.

Para instruções detalhadas sobre a execução do projeto, consulte [Como Executar](ComoExecutar.md).

# Documentos

* Relatório técnico [relatorio.pdf](Relatório%20P002.pdf)
* Apresentação: [apresentacao.pdf](Apresentação%20P002.pdf) 

## 🧪 Técnicas Implementadas

As seguintes técnicas de busca heurística foram implementadas:

### 🔍 Busca Local

A busca local avalia os vizinhos dos centróides para identificar configurações que reduzam o custo total. Quando um vizinho proporciona menor custo, o algoritmo pode superar mínimos locais encontrados pelo K-Means, embora esteja limitado ao espaço de busca local, podendo convergir para um "mínimo local melhor". Duas variantes foram implementadas:

- **Primeira Melhora**: interrompe a exploração ao encontrar o primeiro vizinho com custo inferior.
- **Melhor Melhora**: analisa todos os vizinhos e seleciona o de menor custo.

### 🔍 Busca Tabu

A busca tabu aprimora a busca local ao incorporar uma lista tabu, uma memória que evita revisitar soluções recentes. Isso amplia a exploração do espaço de busca e facilita a superação de mínimos locais. Um critério de aspiração foi implementado, permitindo aceitar uma solução tabu se ela superar a melhor solução conhecida, aumentando as chances de alcançar o ótimo global.

## 📊 Vizinhanças

Duas estruturas de vizinhança foram definidas:

- **Vizinhança VPS (Passo Simples)**: cada centróide gera 8 vizinhos, totalizando 512 combinações.
- **Vizinhança VPD (Passo Duplo)**: cada centróide gera 24 vizinhos, resultando em 13.824 combinações.

## Fatores que Influenciam o Desempenho

O desempenho das técnicas depende de diversos fatores:

- **Vizinhança**: A qualidade dos centróides encontrados está ligada ao design da vizinhança. Passos pequenos podem restringir a exploração, enquanto passos grandes podem torná-la ineficiente.
- **Número de Iterações**: Mais iterações elevam a probabilidade de encontrar soluções melhores.
- **Parâmetros da Busca Tabu**: O tamanho da lista tabu e o critério de aspiração afetam o desempenho. Uma lista curta pode causar ciclos, enquanto uma longa pode limitar a exploração.

## Cenários Possíveis

- **Melhor Solução pelo K-Means**: Se os centróides iniciais do K-Means estiverem próximos do ótimo global, as buscas local e tabu podem não trazer melhorias significativas.
- **Melhor Solução pela Busca Local/Tabu**: Se o K-Means convergir para um mínimo local distante do ótimo global, as heurísticas têm maior chance de encontrar configurações superiores.

## Exemplo Numérico/Experimental

Um exemplo ilustrativo dos resultados obtidos é apresentado abaixo:

1. **K-Means**: Custo final de 1000.5.
2. **Busca Local**: Reduziu o custo para 950.3, partindo dos centróides do K-Means.
3. **Busca Tabu**: Alcançou um custo de 940.7 com a mesma inicialização.

## 📈 Exemplos de Resultados

Resultados experimentais destacam a eficácia das técnicas:

- **K-Means Inicial**: Custo = 93.3534
- **Busca Local (Melhor Melhora com VPD)**: Custo = 92.2274
- **Busca Tabu (com VPD)**: Custo = 92.2274

Esses valores demonstram que as heurísticas aprimoraram consistentemente a solução inicial do K-Means.

## Conclusão

As técnicas de busca local e busca tabu mostraram-se eficazes para refinar as soluções de agrupamento do K-Means, especialmente em casos de convergência a mínimos locais subótimos. O sucesso depende da inicialização do K-Means e da configuração adequada dos parâmetros, como o design da vizinhança e o tamanho da lista tabu. Experimentos empíricos, aliados à visualização da convergência e históricos de custo, são fundamentais para analisar a evolução das soluções e otimizar os algoritmos.

## 👥 Autores

- Breno Vambáster Cardoso Lima
- Artur Pereira Neto

## Resultados Obtidos

Para um resumo detalhado dos resultados, consulte [melhor_resultado.md](melhor_resultado.md).