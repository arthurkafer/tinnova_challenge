
# tinnova_challenge

Este projeto é um desafio da **Tinnova** e consiste vários scripts para resolução dos desafios pedidos. 4 deles são scripts simples em Python com comentários onde julguei necessário e o último (5) é um servicinho com backend e frontend

- Uma API RESTful desenvolvida em Python com Flask
- Um frontend simples em modo single page app

## Como testar

1. Clone o repositório:
   ```bash
   git clone https://github.com/arthurkafer/tinnova_challenge.git
   cd tinnova_challenge
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie a aplicação:
   ```bash
   python3 src/server.py
   ```

## Sobre o cadastro de veículos (5)

A aplicação permite:

- Cadastro, edição e exclusão de veículos
- Consulta de veículos não vendidos
- Estatísticas por década de fabricação e por fabricante
- Listagem de veículos cadastrados na última semana
- Validação de marcas: somente nomes corretos são aceitos

Todos os requisitos especificados no desafio foram implementados.
