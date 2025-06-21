from driver import options, service
from selenium.webdriver import Chrome
from params_pipeline import *
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re


# Instancia o WebDriver

driver = Chrome(service=service)
driver.get('https://www.sofascore.com/pt/time/futebol/atletico-mineiro/1977') 
time.sleep(3)


# Obtem os dados brutos dos jogos via XPATH ou CSS_SELECTOR

xpath = r'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[2]/div'
xpath_anterior = r'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[1]/div[1]/button/span'
lines = []
padrao = re.compile(r"\d\d/\d\d/24")

while True:
    raw = driver.find_element(By.XPATH, xpath).text
    lines.append(raw)

    # Se eu já vi "/24" dentro desse raw, interrompo antes de clicar
    if ano_limite in raw:
        break

    # Caso contrário, tento ir para a página anterior
    try:
        anterior = driver.find_element(By.XPATH, xpath_anterior)
        anterior.click()
        time.sleep(2)  # dá um tempinho para a página recarregar
    except:
        print("Botão anterior não encontrado. Encerrando loop.")
        break



dados_nao_estruturados = pd.DataFrame(lines, columns=["div"])
dados_nao_estruturados.to_csv("pipeline1.csv")