- [Repositório de Técnicas de Busca Heurística](#repositório-de-técnicas-de-busca-heurística)
  - [Estrutura do Repositório](#estrutura-do-repositório)
  - [Descrição dos Projetos](#descrição-dos-projetos)
    - [Projeto P002](#projeto-p002)
      - [Metodologia](#metodologia)
      - [Resultados](#resultados)
      - [Acesso aos Detalhes](#acesso-aos-detalhes)
    - [Projeto P003](#projeto-p003)
      - [Metodologia](#metodologia-1)
      - [Resultados](#resultados-1)
      - [Acesso aos Detalhes](#acesso-aos-detalhes-1)
  - [Análise Comparativa](#análise-comparativa)
- [Requisitos](#requisitos)
- [Autores](#autores)
- [Observações](#observações)

# Repositório de Técnicas de Busca Heurística

Este repositório reúne os projetos desenvolvidos no âmbito da disciplina **Técnicas de Busca Heurística**, integrante do curso de Ciência da Computação do **Instituto Federal do Norte de Minas Gerais (IFNMG)**. Os projetos, denominados **P002** e **P003**, abordam a otimização de um problema de agrupamento baseado em centróides, utilizando a base de dados **Wine**, reduzida a duas dimensões (ℝ²) com os atributos **Flavonoides** e **Fenóis Totais**. O objetivo central é minimizar a soma das distâncias euclidianas dos registros aos seus respectivos centróides, refinando soluções iniciais obtidas pelo algoritmo **K-Means** por meio de abordagens heurísticas distintas.

## Estrutura do Repositório

O repositório está organizado em dois subdiretórios, correspondentes aos projetos desenvolvidos:

- **[P002](./P002)**: Dedica-se à aplicação de técnicas de busca local e busca tabu.
- **[P003](./p003)**: Concentra-se na utilização de algoritmos genéticos.

Detalhes sobre a implementação e execução de cada projeto podem ser encontrados nos respectivos arquivos `README.md` e, no caso do P002, no documento complementar `ComoExecutar.md`.

## Descrição dos Projetos

### Projeto P002

O Projeto P002 investiga a aplicação de técnicas de **busca local** (nas variantes de primeira melhora e melhor melhora) e **busca tabu** para otimizar o posicionamento de três centróides no problema de agrupamento. Essas abordagens buscam superar os mínimos locais identificados pelo algoritmo K-Means, explorando configurações alternativas de centróides por meio de estruturas de vizinhança.

#### Metodologia
- **Busca Local**:
  - **Primeira Melhora**: Adota o primeiro vizinho com custo inferior ao da solução atual.
  - **Melhor Melhora**: Avalia todos os vizinhos e seleciona aquele com menor custo.
- **Busca Tabu**: Incorpora uma lista tabu para evitar a revisitação de soluções recentes, com um critério de aspiração que permite aceitar soluções tabu se superiores à melhor solução conhecida.
- **Estruturas de Vizinhança**:
  - VPS (Passo Simples): Gera 8 vizinhos por centróide, totalizando 512 combinações.
  - VPD (Passo Duplo): Produz 24 vizinhos por centróide, resultando em 13.824 combinações.

#### Resultados
As técnicas implementadas reduziram o custo inicial do K-Means (93.3534). A busca tabu obteve o melhor desempenho, alcançando um custo de 92.2274 com a vizinhança VPD, evidenciando sua capacidade de explorar eficientemente o espaço de soluções.

#### Acesso aos Detalhes
- Diretório: [P002](./P002)
- Documentação: [README](./P002/README.md)
- Instruções de execução: [ComoExecutar.md](./P002/ComoExecutar.md)

### Projeto P003

O Projeto P003 explora a aplicação de **algoritmos genéticos** para o mesmo problema de agrupamento, avaliando duas estratégias de cruzamento para gerar novas soluções a partir de uma população inicial de centróides.

#### Metodologia
- **Algoritmos Genéticos**:
  - **População Inicial**: Composta por 20 indivíduos, incluindo a solução ótima do K-Means e 19 centróides gerados aleatoriamente.
  - **Função de Avaliação**: Calcula a soma das distâncias euclidianas dos registros aos centróides de cada indivíduo.
  - **Cruzamento**:
    - **P001**: Gera um filho pela média das coordenadas dos pais, produzindo 10 novos indivíduos por geração.
    - **P002**: Gera dois filhos por par de pais, trocando coordenadas de dois centróides, resultando em 20 novos indivíduos.
  - **Mutação**: Aplica alterações aleatórias às coordenadas com probabilidade de 0,03, dentro de um intervalo predefinido.
  - **Seleção**: Adota elitismo, preservando os 20 melhores indivíduos por geração com base na função de avaliação.

#### Resultados
Os algoritmos genéticos aprimoraram a solução inicial do K-Means (custo de 93.7869), mas não superaram o desempenho da busca tabu do Projeto P002. A abordagem P001 alcançou um custo de 92.5435 após 500 gerações, enquanto a P002 obteve 92.6674, sugerindo que a média das coordenadas preserva melhor as características de soluções promissoras.

#### Acesso aos Detalhes
- Diretório: [P003](./P003)
- Documentação: [README](./p003/README.md)

## Análise Comparativa

A tabela abaixo sintetiza os resultados obtidos nos dois projetos, comparando os custos finais com a solução de referência do K-Means:

| Método                        | Projeto | Custo       | Redução Relativa ao K-Means |
|-------------------------------|---------|-------------|-----------------------------|
| K-Means (Referência)          | P002    | 93.3534     | -                           |
| Busca Local (Primeira Melhora)| P002    | 93.308      | 0,0486%                     |
| Busca Local (Melhor Melhora)  | P002    | 92.3988     | 1,0226%                     |
| Busca Tabu                    | P002    | 92.2274     | 1,2062%                     |
| K-Means (Referência)          | P003    | 93.7869     | -                           |
| Algoritmo Genético P001       | P003    | 92.5435     | ~1,03%                      |
| Algoritmo Genético P002       | P003    | 92.6674     | ~0,92%                      |

A busca tabu (P002) destacou-se como a abordagem mais eficaz, devido à sua capacidade de escapar de mínimos locais e explorar amplamente o espaço de soluções. Os algoritmos genéticos (P003), embora tenham aprimorado a solução inicial, apresentaram desempenho inferior, possivelmente devido à sensibilidade aos parâmetros de configuração.

# Requisitos
Os projetos requerem a instalação do Python e das dependências listadas nos arquivos requirements.txt de cada diretório. Recomenda-se o uso de ambientes virtuais para isolar as dependências.

# Autores

- Artur Pereira Neto
- Breno Vambáster Cardoso Lima

# Observações
Verifique se o Python e o pip estão devidamente instalados antes de executar os projetos.
Resultados detalhados podem ser encontrados em arquivos específicos, como melhor_resultado.md no diretório do Projeto P002
