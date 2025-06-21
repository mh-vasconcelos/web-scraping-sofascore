from driver import *
from params_pipeline import *
from funcs import *
from selenium.webdriver.common.by import By
import pandas as pd
import time


# 1) Carregar dados não estruturados
df = pd.read_csv('pipeline1.csv')

# 2) concatenar todas as linhas da coluna 'div' em uma única string
raw = df['div'].str.cat(sep="\n")

# 3) dividir em linhas
lines = raw.split("\n")

# 4) Criar dicionário
data = {
    "data": [],
    "time_casa": [],
    "time_fora": [],
    "placar_casa": [],
    "placar_fora": [],
    "campeonato": [],
    "status": [],
    "resultado": []
}

# 5) classe editora da pipeline
processor = Pipeline2Processor(data_dict=data)

camp_atual = None
i = 0

while i < len(lines):
    line = lines[i]

    # 1) DETECTA NOME DE CAMPEONATO
    # Se a linha não for data, mas a próxima for data OU horário, 
    # usamos essa linha como nome do campeonato.
    prox = lines[i + 1] if (i + 1 < len(lines)) else None
    if (
        not processor.is_date(line)
        and (prox is not None)
        and (processor.is_date(prox) or eh_hora(prox))):
        camp_atual = line
        i += 1
        continue

    # 2) SE FOR UMA DATA
    if processor.is_date(line):
        date   = line
        status = lines[i + 1] if (i + 1 < len(lines)) else None
        home   = lines[i + 2] if (i + 2 < len(lines)) else None
        away   = lines[i + 3] if (i + 3 < len(lines)) else None

        # 2.1) CASO: status é só horário (jogo não rolou, sem placar)
        if eh_hora(status):
            # pula data, status, home e away
            i += 4
            continue

        # 2.2) CASO: status indica jogo ocorrido, vamos parsear placar
        base_placar_idx = i + 4
        score_casa, score_fora, resultado, inc_placar = parsear_placar(lines, base_placar_idx)

        # Se parsear_placar não encontrou nada (inc_placar == 0), 
        # consideramos que não há placar nem resultado. 
        # Nesse caso, definimos valores padrão:
        if inc_placar == 0:
            score_casa = None
            score_fora = None
            resultado  = None
            inc_placar  = 4  # apenas date, status, home, away

        # 2.3) ADICIONA NOS DICIONÁRIOS
        data["data"].append(date)
        data["status"].append(status)
        data["time_casa"].append(home)
        data["time_fora"].append(away)
        data["placar_casa"].append(score_casa)
        data["placar_fora"].append(score_fora)
        data["campeonato"].append(camp_atual)
        data['resultado'].append(resultado)

        # 2.4) AVANÇA O ÍNDICE
        i += inc_placar

    else:
        # linhas que não são data nem campeonato: apenas avança
        i += 1

# Pequena pausa (mesmo comportamento do original)
time.sleep(5)

# Monta DataFrame e exporta
df_result = pd.DataFrame(data)
df_result.to_csv("pipeline2.csv", index=False)

