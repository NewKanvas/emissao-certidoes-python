import json
import os
from Certidoes.RFB_PGFN import *

# Carregar os dados do JSON (Teste)

# Json selecionado
fjson = "dados.json"
with open(f"Python-certidao-emissao\Data\{fjson}", "r", encoding="utf-8") as file:
    dados = json.load(file)


# Corrigindo possiveis erros do JSON
def corrigir_dados_json(data):
    # Substituir dados vazios por zero
    for chave, valor in data.items():
        if valor.strip() == "" or valor.strip() == "_":
            data[chave] = "0"
    # Tirando espaços do CPF
    if "cpf" in data:
        cpf = data["cpf"].strip().replace(".", "").replace("-", "")
        data["cpf"] = cpf
    return data


# os.system("cls")
dados = corrigir_dados_json(dados)

# RFB_PGFN(**dados).show()
RFB_PGFN(**dados).emitir()
# RFB_PGFN(**dados).emitir_relatorio()
