# **Automação de Emissão de Certidões - Python**

Este projeto visa automatizar a emissão de certidões utilizando Python, sem interface gráfica. O script desenvolvido permitirá a emissão de diferentes tipos de certidões, conforme especificado abaixo.

### **Certidões Disponíveis:**

1. **[Certidão Regularidade Fiscal PF (RFB e PGFN)](https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/EmitirPGFN)**

2. **[Certidão de Regularidade Fiscal SEFAZ/RJ](https://www4.fazenda.rj.gov.br/certidao-fiscal-web/emitirCertidao.jsf)**

3. **[Certidão de Regularidade Fiscal SEFAZ/ES](https://s2-internet.sefaz.es.gov.br/certidao/cnd)**

4. **[RIO: Dívida Ativa Mun.](https://daminternet.rio.rj.gov.br/certidao/Requerimento)**

5. **[Certidão Negativa de Débitos de Tributos Municipais (Vitória)](https://tributario.vitoria.es.gov.br/Servicos/CertidaoNegativa/CertidaoNegativa.aspx)**

6. **[Certidão Negativa da Justiça Federal do TRF-2 (Cível)](https://certidoes.trf2.jus.br/certidoes/#/principal/solicitar)**

7. **[Certidão Negativa da Justiça Federal do TRF-2 (Criminal)](https://certidoes.trf2.jus.br/certidoes/#/principal/solicitar)**

8. **[Certidão negativa no TJES](https://sistemas.tjes.jus.br/certidaonegativa/sistemas/certidao/CERTIDAOPESQUISA.cfm)**

### Funcionalidades:

- Orquestração da emissão de todas as certidões através de uma função.
- Integração com um webservice existente.
- Possibilidade de especificar quais certidões devem ser emitidas ou emitir todas.
- Parâmetros necessários fornecidos via estrutura JSON.
- Validação dos dados fornecidos para cada certidão.
- Geração de relatório com informações sobre o processo de emissão.

### Identificador Único do JOB:

Cada JOB terá um identificador único no formato: `no_proc_pagamento_primeiro_nome_cpf_sequencial`.

Exemplo: `50232501320214029388_bruna_07898745325_01`

### Armazenamento dos Arquivos:

Cada JOB criará uma pasta com seu ID dentro de uma pasta-mãe denominada "JOBS", para armazenar os arquivos necessários.

### Envio de E-mail:

Um e-mail com o resultado do JOB e os PDFs das certidões será enviado para `yyyy`, copiando para `xxxx`.

### Serviço Anti-Captcha:

Para ultrapassar os reCAPTCHA do Google, será utilizado o serviço [anti-captcha.com](https://anti-captcha.com/pt).
