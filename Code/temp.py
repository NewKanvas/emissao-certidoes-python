# Imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# from selenium_stealth import stealth  # pip install selenium-stealth
import undetected_chromedriver as uc  # pip install undetected-chromedriver

import time
import os
import shutil

from utils import *

# ---

# Configuração do ChromeOptions
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Dados

no_proc_pagamento = "1234567890"  # teste
url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN"
cpf = "xxxxxxx"  # Trocar para um CPF valido
primeiro_nome = "Jonas"  # teste
id = "1"
id_job = f"{no_proc_pagamento}_{primeiro_nome}_{cpf}_{id}.pdf"

log = []

# ---

# Inicialização do ChromeDriver
driver = uc.Chrome(use_subprocess=True, headless=False)

# Realizar as operações no navegador
driver.get(url)
logprint("Abrindo navegador...", log)
time.sleep(2)

# Preencher o campo CPF
cpf_input = driver.find_element("xpath", '//*[@id="NI"]')
logprint("Preenchendo CPF...", log)

# Certificando que CPF foi digitado corretamente
i = 0
while remove_format(cpf_input.get_attribute("value")) != cpf:
    cpf_input.clear()
    cpf_input.send_keys(cpf)
    # write(cpf, cpf_input)

    # Limite de tentativas
    i += 1
    if i >= 10:
        logprint(
            f"Não foi possível concluir a operação, houve um erro com o CPF.\nPor favor, confirme se o CPF {cpf} está correto.\nAbortando operação.",
            log,
        )
        driver.quit()
        exit()

# Clicar no botão para validar
driver.find_element("xpath", '//*[@id="validar"]').click()
time.sleep(5)

try:
    # Verificar se da para emiter outra certidão
    ncertidao = driver.find_element(
        "xpath", "/html/body/div[1]/div/table/tbody/tr/td/form/a[2]"
    )
    ncertidao.click()
    time.sleep(5)

except NoSuchElementException:  # Se nao achar:
    logprint("Tentando Emitir Certidao Normalmente...", log)

finally:
    try:
        # Esperar até que ache o elemento
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div/table/tbody/tr/td/div/a[1]/input',
                )
            )
        )
        logprint("Verificação concluida, finalizando em 15 segundos...", log)

    except NoSuchElementException:  # Se nao achar:
        logprint("Excesso de tentativas, finalizando código...", log)

    time.sleep(15)  # Esperar um pouco, para concluir possiveis downloads
    # Tendo certeza que o navegador fechous
    try:
        driver.quit()
    except WebDriverException:
        pass

# **Movendo PDF da certidão**

# Configurando pasta de Download

dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Data", "Jobs", no_proc_pagamento)
)
# Se nao existir cria:
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

file_name = f"Certidao-{cpf}.pdf"

downloaded_file_path = os.path.join(downloads_dir, file_name)

logprint("Verificando se o PDF está sendo usado por algum processo...", log)
killprov(downloaded_file_path, log)  # Fechando intancias com o pdf aberto

# Verificar se o arquivo foi baixado
if os.path.exists(downloaded_file_path):
    # Mover o arquivo para o diretório especificado
    try:
        shutil.move(downloaded_file_path, os.path.join(dir_path, id_job))
        logprint(f"Arquivo '{file_name}' movido para '{dir_path}'.", log)
        logprint(f"O Arquivo '{file_name}' foi renomeado para '{id_job}'.", log)
    except Exception as e:
        logprint(f"Erro ao mover o arquivo: {e}", log)
else:
    logprint(f"Arquivo '{file_name}' não encontrado na pasta de downloads.", log)

logs_dir = os.path.join(dir_path, "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_path = os.path.join(logs_dir, "log1.txt")

with open(log_path, "w", encoding="utf-8") as file:
    for message in log:
        file.write(message + "\n")
