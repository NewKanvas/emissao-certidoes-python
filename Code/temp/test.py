from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)  # Abrindo navegador
navegador.get(
    "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN"
)


navegador.find_element("xpath", '//*[@id="NI"]').send_keys("12345678909")
navegador.find_element("xpath", '//*[@id="validar"]').click()


time.sleep(20)
