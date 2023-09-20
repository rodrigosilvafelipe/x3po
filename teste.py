import os
import re
import fitz
import json
import openpyxl
import math
import time
import pandas as pd
import smtplib

from datetime import datetime
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, numbers, NamedStyle

def leitorPgdasD(path):

    # path = input("Digite o caminho da pasta: ")
    # pathXlsx = input("Digite o caminho da planilha de controle: ")
    # print("Digite o valor do salário mínimo atual. Utilize ponto '.' como separador de centavos. Não utilize vírgula ',' nem separador de milhar. Exemplo: 1320.00")
    # salarioMinimo = float(input("Salário mínimo atual: "))

    # if os.path.isdir(path):
    #     print("Processo iniciado.")
    # else:
    #     print("Caminho da pasta inválido.")
    #     time.sleep(5)
    #     exit()

    # caminho para a pasta contendo os arquivos PDF
    pasta = path

    # expressão regular para extrair o Período de Apuração
    periodoApuracao_regex = r"Período de Apuração:(.*?)\n\.\n1\. Identificação do Contribuinte"

    # expressão regular para extrair o nome empresarial do PDF
    nome_empresarial_regex = r"Nome empresarial:(.*?)Data de abertura no CNPJ:"

    # expressão regular para extrair o CNPJ do PDF
    cnpj_regex = r"CNPJ Matriz:(.*?)Nome empresarial:"

    # expressão regular para extrair a data de abertura no CNPJ
    aberturaCnpj_regex = r"Data de abertura no CNPJ:(.*?)Optante pelo Simples Nacional:"

    # expressão regular para extrair o N° da Declaração
    nDeclaracao_regex = r"Nº da Declaração:(.*?)1.1 CNPJ das filiais presentes nesta declaração:"

    # expressão regular para extrair a RPA
    rpa_regex = r"Receita Bruta do PA \(RPA\) - Competência(.*?)Receita bruta acumulada nos doze meses anteriores"

    # expressão regular para extrair a RBT12
    rbt12_regex = r"ao PA \(RBT12\)(.*?)Receita bruta acumulada nos doze meses anteriores\nao PA proporcionalizada \(RBT12p\)"

    # expressão regular para extrair a RBT12p
    rbt12p_regex = r"Receita bruta acumulada nos doze meses anteriores\nao PA proporcionalizada \(RBT12p\)(.*?)Receita bruta acumulada no ano-calendário corrente"

    # expressão regular para extrair as Receitas Brutas Anteriores Mercado Interno
    rbaInterno_regex = r"2\.2\.1\) Mercado Interno(.*?)2\.2\.2\) Mercado Externo"

    # expressão regular para extrair as Receitas Brutas Anteriores Mercado Externo
    rbaExterno_regex = r"2\.2\.2\) Mercado Externo(.*?)2\.3\) Folha de Salários Anteriores"

    # expressão regular para extrair as Folhas de Salários Anteriores
    fopag_regex = r"2\.3\) Folha de Salários Anteriores \(R\$\)(.*?)(2\.3\.1\) Total de Folhas de Salários Anteriores|2.4\) Fator r)"

    # expressão regular para extrair o total das Folhas de Salários Anteriores
    fopagTotal_regex = r"2\.3\.1\) Total de Folhas de Salários Anteriores \(R\$\)  R\$ (.*?)\n"

    # expressão regular para extrair o Fator R
    fatorR_regex = r"Fator r \= (.*?)(Número da Declaração:|2\.5\) Valores Fixos)"

    # expressão regular para extrair o Total do Débito Exigível
    debitoExigivel_regex = r"2\.8\) Total Geral da Empresa(.*?)da Recepção da Declaração"

    listaDados = []

    i = 2

    # Cria um novo arquivo XLSX
    # workbook = openpyxl.Workbook()

    # Seleciona a planilha ativa (por padrão, é criada uma planilha chamada "Sheet")
    # sheet = workbook.active

    # Escreve dados na planilha
    # sheet["A1"] = "cnpj"
    # sheet["B1"] = "razao_social"
    # sheet["C1"] = "abertura"
    # sheet["D1"] = "competencia"
    # sheet["E1"] = "valor_faturamento"
    # sheet["F1"] = "faturamento_12_meses_PGDASD"
    # sheet["G1"] = "valor_simples_nacional"
    # sheet["H1"] = "valor_cpp"
    # sheet["I1"] = "folha_acumulada"
    # sheet["J1"] = "fator_R"
    # sheet["K1"] = "proxima_folha"

    # criar objeto NamedStyle
    # contabil_style = NamedStyle(name='contabil')
    # contabil_style.number_format = '#,##0.00_);(#,##0.00)'

    # percorrer os arquivos na pasta
    # for nome_arquivo in os.listdir(pasta):
    try:
        if path.endswith(".pdf"):
            
            # abrir o arquivo PDF
            caminho_arquivo = path
            with fitz.open(caminho_arquivo) as pdf:
                pdf_text = ''
                for pagina in pdf:
                    # extrair o texto da página
                    texto = pagina.get_text()
                    pdf_text += str(texto)

                # usar expressão regular para extrair o Período de Apuração
                match_periodoApuracao = re.search(
                    periodoApuracao_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o nome empresarial
                match_nome_empresarial = re.search(
                    nome_empresarial_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o cnpj
                match_cnpj = re.search(cnpj_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair a data de abertura no CNPJ
                match_aberturaCnpj = re.search(
                    aberturaCnpj_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o Número da Declaração
                match_nDeclaracao = re.search(
                    nDeclaracao_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor da Receita Bruta Atual
                match_rpa = re.search(rpa_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor da Receita Bruta RBT12
                match_rbt12 = re.search(rbt12_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor da Receita Bruta Proporcionalizada RBT12P
                match_rbt12p = re.search(rbt12p_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor das Receitas Brutas Anteriores Mercado Interno
                match_rbaInterno = re.search(
                    rbaInterno_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor das Receitas Brutas Anteriores Mercado Externo
                match_rbaExterno = re.search(
                    rbaExterno_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor da Folha de Pagamento
                match_fopag = re.search(fopag_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor total da Folha de Pagamento
                match_fopagTotal = re.search(
                    fopagTotal_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor do Fator R
                match_fatorR = re.search(fatorR_regex, pdf_text, re.DOTALL)

                # usar expressão regular para extrair o valor do Total do Débito Exigível
                match_debitoExigivel = re.search(
                    debitoExigivel_regex, pdf_text, re.DOTALL)

                if match_periodoApuracao:
                    periodoApuracao = match_periodoApuracao.group(
                        1).strip()

                if match_nome_empresarial:
                    nome_empresarial = match_nome_empresarial.group(
                        1).strip()

                if match_cnpj:
                    cnpj = match_cnpj.group(1).strip()

                if match_aberturaCnpj:
                    aberturaCnpj = match_aberturaCnpj.group(1).strip()

                if match_nDeclaracao:
                    nDeclaracao = match_nDeclaracao.group(1).strip()

                if match_rpa:
                    rpa = match_rpa.group(1).strip().split('\n')

                if match_rbt12:
                    rbt12 = match_rbt12.group(1).strip().split('\n')

                if match_rbt12p:
                    rbt12p = match_rbt12p.group(1).strip().split('\n')

                if match_rbaInterno:
                    rbaInterno = match_rbaInterno.group(
                        1).strip().split(" ")
                    # expressão regular para extrair data e valor
                    regexRbaInterno = r'(\d{2}/\d{4})\n([\d\.,]+)'
                    dadosRbaInterno = []  # lista de tuplas para armazenar os pares chave-valor

                    for item in rbaInterno:
                        matches = re.findall(regexRbaInterno, item)
                        if matches:
                            for match in matches:
                                chave = match[0]
                                valor = float(match[1].replace(
                                    '.', '').replace(',', '.'))
                                dadosRbaInterno.append((chave, valor))

                else:
                    dadosRbaInterno = {}

                if match_rbaExterno:
                    rbaExterno = match_rbaExterno.group(
                        1).strip().split(" ")
                    # expressão regular para extrair data e valor
                    regexRbaExterno = r'(\d{2}/\d{4})\n([\d\.,]+)'
                    dadosRbaExterno = []  # lista de tuplas para armazenar os pares chave-valor

                    for item in rbaExterno:
                        matches = re.findall(regexRbaExterno, item)
                        if matches:
                            for match in matches:
                                chave = match[0]
                                valor = float(match[1].replace(
                                    '.', '').replace(',', '.'))
                                dadosRbaExterno.append((chave, valor))

                else:
                    dadosRbaExterno = {}

                if match_fopag:
                    fopag = match_fopag.group(1).strip().split(" ")
                    # expressão regular para extrair data e valor
                    regex = r'(\d{2}/\d{4})\n([\d\.,]+)'
                    dadosFopag = []  # lista de tuplas para armazenar os pares chave-valor

                    for item in fopag:
                        matches = re.findall(regex, item)
                        if matches:
                            for match in matches:
                                chave = match[0]
                                valor = float(match[1].replace(
                                    '.', '').replace(',', '.'))
                                dadosFopag.append((chave, valor))

                else:
                    dadosFopag = {}

                if match_fopagTotal:
                    fopagTotal = match_fopagTotal.group(1).strip()
                else:
                    fopagTotal = 0.00

                if match_fatorR:
                    fatorR = match_fatorR.group(1).strip()
                else:
                    fatorR = ""

                if match_debitoExigivel:
                    debitoExigivel = match_debitoExigivel.group(1).strip()
                    regexTotal = r"Total do Débito Exigível \(R\$\)(.*?)3\. Informações"
                    match_TotalDebitoExigivel = re.search(
                        regexTotal, debitoExigivel, re.DOTALL)
                    if match_TotalDebitoExigivel:
                        totalDebitoExigivel = match_TotalDebitoExigivel.group(
                            1).strip().split("\n")
                        # a = len(totalDebitoExigivel)
                        # b = a - 2
                        # c = a - 6
                        simplesNacional = totalDebitoExigivel[17]
                        inssCpp = totalDebitoExigivel[13]
                else:
                    debitoExigivel = ""

                # Ler planilha de controle mês anterior

                # Use a função read_excel do pandas para ler a planilha XLSX
                # dataframe = pd.read_excel(pathXlsx, sheet_name='bd')

                # Variáveis para armazenar o valor encontrado
                # folha_acumulada = None

                # Variáveis para definir a competencia
                # competencia = periodoApuracao[-10:]
                # data_objeto = datetime.strptime(competencia, "%d/%m/%Y")
                # competencia = data_objeto.strftime("%Y-%m-%d %H:%M:%S")

                # Percorra cada linha do dataframe
                # for indice, linha in dataframe.iterrows():
                    # Verifique se o CNPJ e a competência correspondem aos desejados
                #    timestamp = pd.Timestamp(linha['competencia'])
                #    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                #    if linha['cnpj'] == cnpj and timestamp_str == competencia:
                #        folha_acumulada = linha['fopag_acumulada_12M']
                #        print(f'{cnpj} | {timestamp_str} | {linha["fopag_acumulada_12M"]}')
                #        break  # Se encontrou o valor, pode interromper o loop

                # try:

                    # inssCpp = inssCpp.replace('.', "")
                    # inssCpp = inssCpp.replace(',', ".")
                    # inssCpp = float(inssCpp)
                    # inssCpp = round(inssCpp, 2)

                    # if len(dadosFopag) > 0:
                        # fopagTotal = fopagTotal.replace('.', "")
                        # fopagTotal = fopagTotal.replace(',', ".")
                        # fopagTotal = float(fopagTotal)
                        # fopagTotal = round(fopagTotal, 2)

                        # fopagAntiga = dadosFopag[0][1]
                        # ultimaFopag = dadosFopag[-1][1]

                        # if len(dadosFopag) >= 12:
                        #     proximaFopagTotal = fopagTotal - fopagAntiga + inssCpp

                        # else:
                        #     proximaFopagTotal = fopagTotal + inssCpp

                    # else:
                    #     proximaFopagTotal = 0.00
                    #     ultimaFopag = 0.00
                # except Exception as e:
                #     print(e)

                rbt12Total = rbt12[2]
                # rbt12Total = rbt12[2].replace(".", "")
                # rbt12Total = rbt12Total.replace(",", ".")
                # rbt12Total = float(rbt12Total)
                # rbt12Total = round(rbt12Total, 2)

                rpaTotal = rpa[2]
                # rpaTotal = rpa[2].replace(".", "")
                # rpaTotal = rpaTotal.replace(",", ".")
                # rpaTotal = float(rpaTotal)
                # rpaTotal = round(rpaTotal, 2)

                # print("Até aqui")

                # if len(dadosRbaInterno) >= 12:
                #     dadosRbaInterno = dadosRbaInterno[-12:]
                #     dadosRbaExterno = dadosRbaExterno[-12:]
                #     proximaRbt12 = rbt12Total - \
                #         dadosRbaInterno[0][1] - \
                #             dadosRbaExterno[0][1] + rpaTotal

                # else:
                #     proximaRbt12 = rbt12Total + rpaTotal

                # print("Encontrou tudo")

                # if proximaRbt12 != 0.0:
                #     proximaFopag = proximaRbt12 * 0.2801 - proximaFopagTotal
                #     if proximaFopag != 0.00:
                #         if proximaFopag < salarioMinimo:
                #             proximaFopag = salarioMinimo
                #     proximoFatorR = (proximaFopagTotal + proximaFopag) / proximaRbt12

                # else:
                #     proximaFopag = proximaRbt12 * 0.2801 - proximaFopagTotal
                #     if proximaFopag != 0.00:
                #         if proximaFopag < salarioMinimo:
                #             proximaFopag = salarioMinimo
                #     proximoFatorR = 0.0

                # if rpaTotal == 0.0:
                #     proximaFopag = 0.0

                # if fatorR == "Não se aplica" and rpaTotal != 0.00:
                #     proximaFopag = salarioMinimo

                # proximaRbt12 = round(proximaRbt12, 2)
                # if proximaFopag != 0.0:
                #     if proximaFopag != salarioMinimo:
                #         proximaFopag = math.ceil(proximaFopag)

                # Gera um json com os dados do documento

                # try:

                #     simplesNacional = simplesNacional.replace(".", "")
                #     simplesNacional = simplesNacional.replace(",", ".")
                #     simplesNacional = float(simplesNacional)
                #     simplesNacional = round(simplesNacional, 2)
                # except Exception as e:
                #     print(e)

                listaRpaInterno = [{'chave': t[0], 'valor': t[1]}
                    for t in dadosRbaInterno]
                objetoListaRpaInterno = {
                    d['chave']: d['valor'] for d in listaRpaInterno}
                listaRpaExterno = [{'chave': t[0], 'valor': t[1]}
                    for t in dadosRbaExterno]
                objetoListaRpaExterno = {
                    d['chave']: d['valor'] for d in listaRpaExterno}
                listaFolhas = [{'chave': t[0], 'valor': t[1]}
                    for t in dadosFopag]
                objetoListaFolhas = {d['chave']: d['valor']
                    for d in listaFolhas}
                
                # print("Encontrou tudo")

                # dados = {
                #     "Empresa": nome_empresarial,
                #     "cnpj": cnpj,
                #     "Data de abertura": aberturaCnpj,
                #     "Competência": periodoApuracao[-7:],
                #     "Dados da declaração": {
                #         "Período da apuração": periodoApuracao,
                #         "Número da declaração": nDeclaracao,
                #         "Receita bruta do período de apuração": {
                #             "Mercado Interno": float(rpa[0].replace(".", "").replace(",", ".")),
                #             "Mercado Externo": float(rpa[1].replace(".", "").replace(",", ".")),
                #             "Total": float(rpa[2].replace(".", "").replace(",", ".")),
                #         },
                #         "Receita Bruta Acumulada (RBT12)": {
                #             "Mercado Interno": float(rbt12[0].replace(".", "").replace(",", ".")),
                #             "Mercado Externo": float(rbt12[1].replace(".", "").replace(",", ".")),
                #             "Total": float(rbt12[2].replace(".", "").replace(",", "."))
                #         },
                #         "Receitas anteriores ao PA": {
                #             "Mercado Interno": [objetoListaRpaInterno],
                #             "Mercado Externo": [objetoListaRpaExterno]
                #         },
                #         "Folha de pagamento": {
                #             "Folhas anteriores": [objetoListaFolhas],
                #             "Total folhas anteriores": fopagTotal,
                #             "Fator R": fatorR
                #         },
                #         "Impostos": {
                #             "Simples Nacional": simplesNacional,
                #             "INSS/CPP": inssCpp
                #         },
                #         "Proxima RBT12": proximaRbt12,
                #         # "Proxima Fopag": proximaFopag
                #     }
                # }

                # listaDados.append(dados)

                # receitaPeriodo = rpa[2].replace(".", "")
                # receitaPeriodo = receitaPeriodo.replace(",", ".")
                # receitaPeriodo = float(receitaPeriodo)

                # aberturaCnpj = datetime.strptime(aberturaCnpj, "%d/%m/%Y")
                # periodoApuracao = datetime.strptime(
                #     periodoApuracao[-10:], "%d/%m/%Y")

                # Escreve dados na planilha
                # 

                # print(f"##################################################")
                # print(f"Empresa: {nome_empresarial}")
                # print(f"CNPJ: {cnpj}")
                # print(f"Data de abertura: {aberturaCnpj}")
                # print(f"Número da declaração: {nDeclaracao}")
                # print(f"Receita bruta do período de apuração: {rpa}")
                # print(f"Receita bruta acumulada RBT12: {rbt12}")
                # print(f"Receita bruta acumulada proporcionalizada (RBT12p): {rbt12p}")
                # print(f"Receitas anteriores ao PA - Mercado Interno: {dadosRbaInterno}")
                # print(f"Receitas anteriores ao PA - Mercado Externo: {dadosRbaExterno}")
                # print(f"Folha de pagamento: {dadosFopag}")
                # print(f"Total da Folha de pagamento: {fopagTotal}")---
                # print(f"Fator R: {fatorR}")---
                # print(f"Simples Nacional: {simplesNacional}")---
                # print(f"INSS/CPP: {inssCpp}")---
                # print(f"Próxima RBT12: {proximaRbt12}")
                # print(f"Próxima Fopag: {proximaFopag}")
                # print(pdf_text)
                # else:
                #     print(f"{nome_arquivo}")

                # i += 1

                linha = [
                    "PGDASD",
                    cnpj,
                    nome_empresarial,
                    aberturaCnpj,
                    periodoApuracao,
                    rpa[2],
                    rbt12[2],
                    simplesNacional,
                    inssCpp,
                    fopagTotal,
                    fatorR
                ]

                # Especifique o nome do arquivo de texto
                raiz_cnpj = ''.join(filter(str.isdigit, cnpj))
                arquivo_texto = f"Z:\\RPA\\Simples Nacional\\BD_Simples_Nacional\\{raiz_cnpj}.txt"

                # Texto que você deseja adicionar ao arquivo
                texto_a_adicionar = '|'.join(linha)

                # Verifica se o arquivo já existe
                if not os.path.isfile(arquivo_texto):
                    # Se o arquivo não existir, cria um novo arquivo
                    with open(arquivo_texto, 'w') as arquivo:
                        arquivo.write(texto_a_adicionar)
                else:
                    # Se o arquivo já existir, abre em modo de adição e adiciona uma linha
                    with open(arquivo_texto, 'a') as arquivo:
                        arquivo.write(texto_a_adicionar)

        # print("Pronto")

        return True

    except Exception as e:
        return False
        # print(e)

path = input("Caminho: ")
leitorPgdasD(path)