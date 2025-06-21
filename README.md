# web-scraping-sofascore
Raspagem de dados do site sofascore
## Objetivo:
Coletar informações de um time específico de exemplo (Vasco da Gama) dos últimos jogos dos anos de 2025 e 2024.
Em tese, usamos um ETL, mas na verdade fizemos o processo em duas etapas:
- Primeiro trouxemos os dado de qualquer jeito
- Em seguida estruturamos esses dados para uso

## O processo é dividido em três sub-etapas:
- Carregamento dos dados brutos da página web (dados chegam não estruturados) (extract.py)
- Transformação dos dados em uma tabela estruturada (transform.py)
- Preparação para carregamento em um banco de dados SQLite (load.py)

  ## Sequência dos arquivos
  - params_pipeline.py: responsável por armazenar os parâmetros de url do time escolhido e ano limite de observação
  - driver.py: responsável por armazenar a configuração para estabelecer conexão com a página web
  - extract.py: responsável por estabelecer conexão com a página e salvar os dados não estruturados
  - funcs.py: responsável por armazenar funções e a classe editora dos dados não estruturados para convertê-los em estruturados
  - transform.py: responsável por transformar os dados usando as funções do file anterior
  - load.py: carregar em um banco de dados SQLite

    ## Desafios
    O grande desafio é transformar esses dados não estruturados. Usei uma lógica não trivial para analisar a sequência das informações dos jogos, para encontrar um padrão nos dados não estruturados com o intuito de transformar facilmente em dados estruturados
