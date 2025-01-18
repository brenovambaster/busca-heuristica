
# Como Rodar o Projeto

Este projeto foi desenvolvido em Python e requer a configuração de um ambiente virtual para gerenciar as dependências.

## Pré-requisitos

- Python 3.8 ou superior instalado no sistema.  
  Verifique a instalação do Python no terminal/cmd:
  ```bash
  python --version
  ```

## Passo a Passo para Configuração

1. **Clone o repositório do projeto**  
   Se você ainda não clonou o repositório, use:
   ```bash
   git clone https://github.com/brenovambaster/busca-heuristica.git
   cd busca-heuristica
   cd P002
   ```

2. **Crie um ambiente virtual**  
   No diretório raiz do projeto(dentro de P002), crie o ambiente virtual com:
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**  
   No Windows, ative o ambiente com:
   ```bash
   venv\Scripts\activate
   ```
   Após ativar, o terminal exibirá algo como `(venv)` no início da linha.

4. **Instale as dependências**  
   Com o ambiente virtual ativo, instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o projeto**  
   Após a configuração, você pode executar o projeto. Dependendo do arquivo principal, o comando será algo como:
   ```bash
   python main.py
   ```

## Outras Informações

- Caso você atualize as dependências do projeto, gere um novo `requirements.txt` com:
  ```bash
  pip freeze > requirements.txt
  ```
- Para sair do ambiente virtual, digite:
  ```bash
  deactivate
  ```

Agora você está pronto para usar o projeto! 🚀
