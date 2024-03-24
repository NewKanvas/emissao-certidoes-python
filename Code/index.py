import json
import os


class RFB_PGFN:
    # https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN
    def __init__(self, no_proc_pagamento, nome_completo, cpf, endereco, cidade, uf):
        self.no_proc_pagamento = no_proc_pagamento
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.endereco = endereco
        self.cidade = cidade
        self.uf = uf

    def show(self):
        print(f"Número do processo: {self.no_proc_pagamento}")
        print(f"Nome completo: {self.nome_completo}")
        print(f"CPF: {self.cpf}")
        print(f"Endereço: {self.endereco}")
        print(f"Cidade: {self.cidade}")
        print(f"UF: {self.uf}")

    def emitir(self):
        # Renomeando "PDFs"
        id = "01"
        primeiro_nome = self.nome_completo.split()[0]
        id_job = f"{self.no_proc_pagamento}_{primeiro_nome}_{self.cpf}_{id}"

        # Caminho do arquivo
        dirname = os.path.dirname(__file__)  # Diretorio atual
        pasta = os.path.join(
            dirname, "..", "Data", "Jobs", self.no_proc_pagamento
        )  # Caminho Relativo
        os.makedirs(pasta, exist_ok=True)  # Cria a pasta se não existir

        # Criando o arquivo na pasta Jobs com nome selecionado
        caminho_arquivo = os.path.join(pasta, f"{id_job}.pdf")  # arquivo teste
        with open(caminho_arquivo, "w") as f:
            pass

    def emitir_relatorio(self):
        # Criando Relatorio
        primeiro_nome = self.nome_completo.split()[0]
        id_relatorio = f"{self.no_proc_pagamento}_{primeiro_nome}_{self.cpf}_relatorio"

        # Caminho do arquivo
        dirname = os.path.dirname(__file__)  # Diretorio atual
        pasta = os.path.join(
            dirname, "..", "Data", "Jobs", self.no_proc_pagamento
        )  # Caminho Relativo
        os.makedirs(pasta, exist_ok=True)  # Cria a pasta se não existir

        # Verifica se algum dado está vazio e registra a ocorrência no relatório
        dados_vazios = []
        for key, value in self.__dict__.items():
            if value == "" or value == "0" or value == "_":
                dados_vazios.append(key)

        # Verifica se o arquivo foi criado/salvo.
        id_job = f"{self.no_proc_pagamento}_{primeiro_nome}_{self.cpf}_01"
        caminho_arquivo = os.path.join(pasta, f"{id_job}.pdf")
        if os.path.exists(caminho_arquivo):
            status_pdf = "PDF gerado corretamente."
        else:
            status_pdf = "Houve um erro ao gerar o PDF."

        # Relatorio
        with open(
            os.path.join(pasta, f"{id_relatorio}.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(
                "Relatório de Emissão de Certidão Regularidade Fiscal PF (RFB e PGFN)\n\n"
            )
            f.write(f"Número do processo: {self.no_proc_pagamento}\n")
            f.write(f"Nome completo: {self.nome_completo}\n")
            f.write(f"CPF: {self.cpf}\n")
            f.write(f"Endereço: {self.endereco}\n")
            f.write(f"Cidade: {self.cidade}\n")
            f.write(f"UF: {self.uf}\n")
            f.write("\n")
            # Verificando Dados vazios
            if dados_vazios:
                f.write("Dados não prenchidos corretamente:\n")
                for dado in dados_vazios:
                    f.write(f"- {dado}\n")
                f.write("\n")
            # Verificando CPF
            if len(self.cpf) != 11 or not self.cpf.isdigit():
                f.write("CPF inválido")
            # Verificando Status do PDF
            f.write(f"Status do PDF: {status_pdf}\n")


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
RFB_PGFN(**dados).emitir_relatorio()

"""
# https://www4.fazenda.rj.gov.br/certidao-fiscal-web/emitirCertidao.jsf 
class SEFAZ_RJ :
    def __init__(self, cpf):
    self.cpf = cpf

# https://s2-internet.sefaz.es.gov.br/certidao/cnd 
class SEFAZ_ES :
    def __init__(self, cpf):
    self.cpf = cpf

# https://daminternet.rio.rj.gov.br/certidao/Requerimento
class RIO_DA :
    def __init__(self, cpf):
    self.cpf = cpf

# https://tributario.vitoria.es.gov.br/Servicos/CertidaoNegativa/CertidaoNegativa.aspx
class VIX_DA :
    def __init__(self, cpf):
    self.cpf = cpf

# https://certidoes.trf2.jus.br/certidoes/#/principal/solicitar
class TRF2_CIVEL :
    def __init__(self, cpf):
    self.cpf = cpf

# https://certidoes.trf2.jus.br/certidoes/#/principal/solicitar
class TRF2_CRIMINAL :
    def __init__(self, cpf):
    self.cpf = cpf

# https://sistemas.tjes.jus.br/certidaonegativa/sistemas/certidao/CERTIDAOPESQUISA.cfm
class TJ_ES :
    def __init__(self, cpf):
    self.cpf = cpf
"""
