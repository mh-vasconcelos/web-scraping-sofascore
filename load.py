import sqlite3
import pandas as pd
# 1) Carrega o CSV gerado pela pipeline
csv_file = 'pipeline2.csv'
df = pd.read_csv(csv_file)

# 2) Conecta (ou cria) o banco SQLite
db_file = 'pipeline.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


create_table_sql = '''
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    status TEXT,
    time_casa TEXT,
    time_fora TEXT,
    placar_casa TEXT,
    placar_fora TEXT,
    campeonato TEXT,
    resultado TEXT
);
'''
cursor.execute(create_table_sql)
conn.commit()

# 4) Prepara o INSERT para cada linha do DataFrame
def insert_row(row):
    insert_sql = '''
    INSERT INTO jogos (data, status, time_casa, time_fora, placar_casa, placar_fora, campeonato, resultado)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    values = (
        row['data'],
        row['status'],
        row['time_casa'],
        row['time_fora'],
        str(row['placar_casa']) if not pd.isna(row['placar_casa']) else None,
        str(row['placar_fora']) if not pd.isna(row['placar_fora']) else None,
        row['campeonato'],
        row['resultado']
    )
    cursor.execute(insert_sql, values)

# 5) Insere todas as linhas
for _, row in df.iterrows():
    insert_row(row)

# 6) Confirma e fecha conexão
conn.commit()
conn.close()