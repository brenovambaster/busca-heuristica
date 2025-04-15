- [📌 Descrição do Projeto](#-descrição-do-projeto)
- [Documentos](#documentos)
- [Algoritmos Genéticos](#algoritmos-genéticos)
- [📊 Abordagem Proposta](#-abordagem-proposta)
- [📈 Resultados e Discussão](#-resultados-e-discussão)
  - [Comparação com Outras Abordagens](#comparação-com-outras-abordagens)
- [Conclusão](#conclusão)
- [👥 Autores](#-autores)
- [Requisitos](#requisitos)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Solução de Problemas](#solução-de-problemas)


## 📌 Descrição do Projeto

Este projeto foi desenvolvido para a disciplina de Técnicas de Busca Heurística do curso de Ciência da Computação do IFNMG - Instituto Federal do Norte de Minas Gerais. Ele explora a aplicação de algoritmos genéticos para otimizar o problema de agrupamento baseado em centróides, utilizando a base de dados Wine reduzida a duas dimensões (R²) com os atributos Flavonoides e Fenóis Totais. O objetivo principal é minimizar o somatório das distâncias euclidianas dos registros aos seus respectivos centróides, definindo um conjunto otimizado de três centróides.

A base de dados Wine, disponibilizada pelo UCI Machine Learning Repository, contém informações sobre características químicas de vinhos de três variedades cultivadas na região da Lombardia, Itália. Neste estudo, a dimensionalidade foi reduzida para facilitar a análise, mantendo apenas os atributos Flavonoides e Fenóis Totais.

## Documentos

* Relatório técnico : [relatorio.pdf](Relatório%20P003.pdf)
* Apresentação: [apresentacao.pdf](ApresentacaoAG.pdf)


## Algoritmos Genéticos

Os algoritmos genéticos (AGs) são métodos de otimização inspirados na evolução biológica e na seleção natural de Darwin. Eles operam sobre uma população de soluções candidatas (representadas como "cromossomos"), refinando-as ao longo de gerações por meio de processos como cruzamento, mutação e seleção. Os principais componentes utilizados neste projeto incluem:

- **População Inicial**: Composta por 20 indivíduos, sendo um deles a solução ótima obtida na etapa anterior (baseada em K-Means) e 19 centróides gerados aleatoriamente dentro do espaço de possibilidades.
- **Função de Fitness**: Calcula a qualidade de cada solução com base na soma das distâncias euclidianas dos pontos aos seus centróides.
- **Cruzamento**: Dois métodos foram testados:
  - **P001**: Gera um filho calculando a média das coordenadas dos pais, produzindo 10 novos indivíduos por geração.
  - **P002**: Gera dois filhos por par de pais, trocando coordenadas de dois dos três centróides, resultando em 20 novos indivíduos por geração.
- **Mutação**: Aplica-se a cada coordenada com uma probabilidade de 0,03. Quando ocorre, a coordenada é ajustada por um valor aleatório \(d\) dentro de um intervalo \([-d_{max}, d_{max}]\).
- **Seleção**: Usa elitismo, preservando os 20 melhores indivíduos de cada geração com base na métrica de avaliação.

## 📊 Abordagem Proposta

A abordagem foi estruturada para otimizar o agrupamento dos dados da base Wine por meio de algoritmos genéticos. Os passos principais incluem:

- **Definição da População**: A população inicial combina a solução ótima da etapa anterior com 19 centróides aleatórios, totalizando 20 indivíduos.
- **Avaliação (Função de Fitness)**: Calcula a soma das distâncias euclidianas dos pontos aos centróides propostos por cada indivíduo.
- **Cruzamento**: Dois métodos foram avaliados:
  - **P001**: Média das coordenadas dos pais para gerar um filho.
  - **P002**: Troca de coordenadas entre dois centróides dos pais para gerar dois filhos.
- **Mutação**: Introduz diversidade ao alterar coordenadas com baixa probabilidade (0,03), evitando convergência prematura.
- **Seleção**: Elitismo seleciona os 20 melhores indivíduos da população total (pais e filhos) para a próxima geração.

## 📈 Resultados e Discussão

Os algoritmos genéticos conseguiram melhorar a solução de referência gerada pelo K-Means (custo inicial de 93.7869), mas não superaram o desempenho das abordagens de busca local e busca tabu aplicadas anteriormente. Os resultados para as duas propostas de cruzamento são apresentados abaixo:

- **Abordagem P001 (um filho por pais)**:
  - Custo após 200 gerações: 92.5308
  - Custo após 500 gerações: 92.5435
- **Abordagem P002 (dois filhos por pais)**:
  - Custo após 200 gerações: 92.7550
  - Custo após 500 gerações: 92.6674

### Comparação com Outras Abordagens
| Método                  | Custo       | Decréscimo em Relação ao K-Means |
|-------------------------|-------------|-----------------------------------|
| K-Means (Referência)    | 93.7869     | -                                 |
| Busca Local (Primeira Melhora) | 93.308 | 0.0486%                   |
| Busca Local (Melhor Melhora) | 92.3988 | 1.0226%                 |
| Busca Tabu              | 92.274      | 1.2062%                   |
| AG P001 (500 gerações)  | 92.5435     | ~1.03%                    |
| AG P002 (500 gerações)  | 92.6674     | ~0.92%                    |

A abordagem P001 apresentou melhor desempenho que a P002, provavelmente porque a média das coordenadas preserva características de boas soluções, enquanto a troca de coordenadas na P002 introduz maior aleatoriedade. Ainda assim, a busca tabu obteve o menor custo (92.274), destacando sua superioridade para este problema.

## Conclusão

Os algoritmos genéticos otimizaram a solução inicial do K-Means, mas não alcançaram o desempenho das técnicas de busca local e busca tabu. A proposta P001 (média das coordenadas) superou a P002 (troca de coordenadas), sugerindo que a preservação de informações de soluções ajustadas é mais eficaz do que a introdução de aleatoriedade excessiva. A menor eficácia dos AGs neste contexto pode estar relacionada à dificuldade de ajustar parâmetros como taxas de mutação e cruzamento, ou à natureza do problema, que favorece métodos baseados em exploração local intensiva, como a busca tabu.

## 👥 Autores

- Artur Pereira Neto
- Breno Vambáster Cardoso Lima

## Requisitos

Consulte os requisitos necessários em [requirements.txt](./requirements.txt).

## Como Executar o Projeto

1. Clone o repositório:
   ```shell
   git clone https://github.com/brenovambaster/busca-heuristica.git
   ```
2. Navegue até o diretório do projeto
    ```shell
    cd busca-heuristica/p003
    ```
3. Crie um ambiente virtual:
    ```shell
    python -m venv venv
    venv\Scripts\activate
    ```
4. Instale as dependências
    ```shell
    pip install -r requirements.txt
    ```
5. Execute o script principal:
   ```
   python main.py
   ```

## Solução de Problemas
Certifique-se de que o Python e o pip estão corretamente instalados.
Verifique se o ambiente virtual está ativado antes de instalar pacotes ou executar o projeto.