from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# from selenium_stealth import stealth  # pip install selenium-stealth
import undetected_chromedriver as uc  # pip install undetected-chromedriver
import time

# import random
import os

# Configuração do ChromeOptions
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Configurando pasta de Download
dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Data", "Jobs")
)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

prefs = {"download.default_directory": dir_path, "safebrowsing.enabled": True}
options.add_experimental_option("prefs", prefs)


## Utils

"""
def sleeper():
    timers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    time.sleep(
        float(
            "0."
            + random.choice(timers[0:3])
            + random.choice(timers[0:4])
            + random.choice(timers[0:9])
        )
    )

for digit in cpf:
    cpf_input.send_keys(digit)
    sleeper()
"""


def remove_format(cpf):
    return "".join(c for c in cpf if c.isdigit())


# Inicialização do ChromeDriver
driver = uc.Chrome(use_subprocess=True, headless=False)

# URL do site
url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN"
# Realizar as operações no navegador

driver.get(url)
time.sleep(2)

# Preencher o campo CPF
cpf_input = driver.find_element("xpath", '//*[@id="NI"]')
cpf = "xxxxxxxxxxx"  # Trocar para um CPF valido

# Certificando que CPF foi digitado corretamente
while remove_format(cpf_input.get_attribute("value")) != cpf:
    cpf_input.clear()
    cpf_input.send_keys(cpf)

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

except NoSuchElementException:
    print("Emitindo Certidao Normalmente...")

finally:
    time.sleep(15)  # Esperar
    driver.quit()
