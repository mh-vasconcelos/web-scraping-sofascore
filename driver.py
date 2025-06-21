import os
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# 1. Desativa a verificação SSL no webdriver-manager se necessário

os.environ['WDM_SSL_VERIFY'] = '0'

# 2. Prepara opções do Chrome
options = Options()

options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# 3. Mantém o navegador aberto se necessário (às vezes a janela do browser automatizado fecha depois de um tempo)
options.add_experimental_option("detach", True)

# 4. Cria o serviço apontando para o driver correto que baixamos do site do google:
# https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br
service = ChromeService("chromedriver.exe", options=options) 