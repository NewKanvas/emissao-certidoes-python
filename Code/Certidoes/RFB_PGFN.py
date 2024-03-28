import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

servico = Service(ChromeDriverManager().install())


class RFB_PGFN:
    # https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN
    def __init__(self, no_proc_pagamento, nome_completo, cpf, endereco, cidade, uf):
        self.no_proc_pagamento = no_proc_pagamento
        self.nome_completo = nome_completo
        self.cpf = cpf  # Só precisa de cpf
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

    def file_path(self):
        # Caminho do arquivo
        dir_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "Data",
                "Jobs",
                self.no_proc_pagamento,
            )
        )
        os.makedirs(dir_path, exist_ok=True)  # Cria a pasta se não existir
        return dir_path

    def emitir(self):
        id = "01"
        primeiro_nome = self.nome_completo.split()[0]
        id_job = f"{self.no_proc_pagamento}_{primeiro_nome}_{self.cpf}_{id}"

        print("Abrindo navegador...")
        navegador = webdriver.Chrome(service=servico)  # Abrindo navegador
        print("Navegador aberto com sucesso.")

        print("Acessando site...")
        navegador.get(
            "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN"
        )
        print("Site acessado.")

        print("Preenchendo CPF...")
        navegador.find_element("xpath", '//*[@id="NI"]').send_keys(f"{self.cpf}")
        print("CPF preenchido.")

        print("Clicando em validar...")
        navegador.find_element("xpath", '//*[@id="validar"]').click()
        print("Validação concluída.")

        print("Esperando...")
        navegador.implicitly_wait(50)

        print("Emitir função concluída.")

    def emitir_relatorio(self):
        # Criando Relatorio
        primeiro_nome = self.nome_completo.split()[0]
        id_relatorio = f"{self.no_proc_pagamento}_{primeiro_nome}_{self.cpf}_relatorio"
        pasta = self.file_path

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
