import os
import re
import fitz
import json
import math
import pandas as pd
from scraping.obterSalarioMinimo import obterSalarioMinimo
from datetime import datetime
from functions.inserirLinhaPlanilha import planilha

def identificaDeclaracao(texto):
    # expressão regular para identificar se é uma declaração do simples nacional
    identificaDeclaracao_regex = r"Programa Gerador do Documento de Arrecadação\ndo Simples Nacional - Declaratório"

    try:

        # usar expressão regular para identificar se é uma declaração do simples nacional
        match_identificaDeclaracao = re.search(identificaDeclaracao_regex, texto, re.DOTALL)

        if match_identificaDeclaracao == None:
            return False
        else:
            return True

    except Exception as e:
            return False
    
def verificaRetencaoIss(pdf_text):
    # O texto que você deseja encontrar
    texto_a_encontrar = "Prestação.de.Serviços,.exceto.para.o.exterior.-.Sujeitos.ao.fator.“r”,.com.retenção/substituição.tributária.de.ISS"

    # Use a função re.search para encontrar o texto no pdf_text
    match = re.search(texto_a_encontrar, pdf_text, re.MULTILINE | re.DOTALL)

    if match:
        # A correspondência foi encontrada, você pode acessar as informações da correspondência usando match.group()
        texto_encontrado = match.group()
        return True
    else:
        return False

def leitorPgdasD(path):

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

    # expressão regular para extrair o tipo de anexo
    sujeitoFatorR_regex = r'Sujeitos ao fator “r”'

    try:
        if path.endswith(".pdf"):
            
            # abrir o arquivo PDF
            caminho_arquivo = path
            with fitz.open(caminho_arquivo) as pdf:
                pdf_text = ''
                for pagina in pdf:
                    # extrair o texto da página
                    texto = pagina.get_text()

                    # Dividir o texto em linhas
                    linhas = texto.split('\n')
                    
                    # Remover as duas últimas linhas
                    if len(linhas) >= 2:
                        linhas = linhas[:-3]
                    
                    # Reconstruir o texto
                    texto_sem_rodape = '\n'.join(linhas)
                    
                    # Adicionar o texto da página ao texto geral
                    pdf_text += texto_sem_rodape
                    pdf_text += '\n'

                if identificaDeclaracao(pdf_text) == False:
                    return ["Erro", "O documento fornecido não é uma declaração do Simples Nacional!"]
                
                issRetido = verificaRetencaoIss(pdf_text)
                
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
                
                # usar expressão regular para extrair o o tipo de tribução com fator R
                match_sujeitoFatorR = re.search(
                    sujeitoFatorR_regex, pdf_text, re.DOTALL)

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
                
                if match_sujeitoFatorR:
                    sujeitoFatorR = "Sim"
                else:
                    sujeitoFatorR = "Não"

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
                    fopagTotal = "0,00"

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
                        if ' ' in totalDebitoExigivel:
                            totalDebitoExigivel.remove(' ')
                        simplesNacional = totalDebitoExigivel[-2]
                        inssCpp = totalDebitoExigivel[-6]
                else:
                    debitoExigivel = ""

                rbt12Total = rbt12[2]

                rpaTotal = rpa[2]

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

                anoCompetenciaProcurada = int(periodoApuracao.split("/")[4]) - 1

                competenciaProcurada = periodoApuracao.split("/")[3] + "/" + str(anoCompetenciaProcurada)

                if len(listaRpaInterno) > 0:

                    chave_encontrada = None
                    for item in listaRpaInterno:
                        if item['chave'] == competenciaProcurada:
                            chave_encontrada = item
                            break

                    if chave_encontrada is not None:
                        receitaInternaSubtrair = chave_encontrada['valor']
                    else:
                        receitaInternaSubtrair = 0

                    chave_encontrada = None
                    for item in listaRpaExterno:
                        if item['chave'] == competenciaProcurada:
                            chave_encontrada = item
                            break

                    if chave_encontrada is not None:
                        receitaExternaSubtrair = chave_encontrada['valor']
                    else:
                        receitaExternaSubtrair = 0

                    receitaSubtrair = receitaInternaSubtrair + receitaExternaSubtrair
                else:
                    receitaSubtrair = 0
                if len(listaFolhas) > 0:
                    
                    folhaQueSai = 0.00

                    if len(listaFolhas) == 12:

                        folhaQueSai = listaFolhas[0]['valor']
                        
                    calcFopagTotal = fopagTotal.replace(".", "")
                    calcFopagTotal = calcFopagTotal.replace(",", ".")
                    calcFopagTotal = float(calcFopagTotal)

                    calcFopagInssCpp = inssCpp.replace(".", "")
                    calcFopagInssCpp = calcFopagInssCpp.replace(",", ".")
                    calcFopagInssCpp = float(calcFopagInssCpp)
                    saldoFopag = calcFopagTotal - folhaQueSai + calcFopagInssCpp
                
                else:
                    saldoFopag = 0
                
                # formatar periodo de apuracao
                inicioMes = periodoApuracao[:10]
                periodoApuracao = periodoApuracao[-10:]

                # formatar fator R
                if fatorR != "Não se aplica":
                    infoFatorR = fatorR.split(" - ")
                    percentualFatorR = infoFatorR[0]
                    anexoFatorR = infoFatorR[1]
                else:
                    percentualFatorR = "0,00"
                    anexoFatorR = "Anexo III"

                # aliquota simples nacional
                totalSimples = simplesNacional.replace(".", "")
                totalSimples = totalSimples.replace(",", ".")
                totalSimples = float(totalSimples)
                receita = rpa[2].replace(".", "")
                receita = receita.replace(",", ".")
                receita = float(receita)
                if totalSimples > 0.00:
                    aliquotaSimples = totalSimples / receita
                    aliquotaSimples = round(aliquotaSimples, 4)
                else: aliquotaSimples = 0

                # formata rbt12 em numero
                rbt12Check = rbt12[2].replace(".", "")
                rbt12Check = rbt12Check.replace(",", ".")
                rbt12Check = float(rbt12Check)

                baseFopag = round((rbt12Check + receita - receitaSubtrair), 2)

                fopagMinima = round(baseFopag, 2) * 0.2801
                
                fopagMinima = round(fopagMinima, 2) - round(saldoFopag, 2)

                fopagMinima = math.ceil(fopagMinima)

                with open("Z:\\RPA\\Folha Pró-Labore\\Salário Mínimo\\Consulta Salario Minimo.json", 'r') as arquivo_json:
                    # Leia o conteúdo do arquivo JSON
                    dados_json = json.load(arquivo_json)

                consultaSalarioData = dados_json[0]['consulta']
                consultaSalarioData = datetime.strptime(consultaSalarioData, "%d/%m/%Y %H:%M:%S")
                
                agora = datetime.now()
                diferenca = agora - consultaSalarioData

                if diferenca.days > 1:
                    obterSalarioMinimo()
                    with open("Z:\\RPA\\Folha Pró-Labore\\Salário Mínimo\\Consulta Salario Minimo.json", 'r') as arquivo_json:
                        # Leia o conteúdo do arquivo JSON
                        dados_json = json.load(arquivo_json)
                
                mes_desejado = periodoApuracao[-7:]
                
                salario_encontrado = None
                
                for item in dados_json:
                    if "periodo" in item and item["periodo"] == mes_desejado:
                        salario_encontrado = item.get("salario")
                        break

                salarioMinimoPeriodo = salario_encontrado.replace(".", "")
                salarioMinimoPeriodo = salarioMinimoPeriodo.replace(",", ".")
                salarioMinimoPeriodo = float(salarioMinimoPeriodo)

                if fopagMinima < salarioMinimoPeriodo:
                    fopagMinima = int(salarioMinimoPeriodo)
                
                if sujeitoFatorR == "Não":
                    fopagMinima = int(salarioMinimoPeriodo)

                linha_dado = [
                    "PGDASD",
                    nDeclaracao,
                    cnpj,
                    nome_empresarial,
                    aberturaCnpj,
                    periodoApuracao[-10:],
                    rpa[0],
                    rpa[1],
                    rpa[2],
                    rbt12[0],
                    rbt12[1],
                    rbt12[2],
                    totalDebitoExigivel[-10],
                    totalDebitoExigivel[-9],
                    totalDebitoExigivel[-8],
                    totalDebitoExigivel[-7],
                    inssCpp,
                    totalDebitoExigivel[-5],
                    totalDebitoExigivel[-4],
                    totalDebitoExigivel[-3],
                    str(simplesNacional),
                    str(aliquotaSimples),
                    fopagTotal,
                    sujeitoFatorR,
                    percentualFatorR,
                    anexoFatorR,
                    str(fopagMinima)
                ]

                def floatExcel(dado):
                    dado = dado.replace(".", "")
                    dado = dado.replace(",", ".")
                    dado = float(dado)
                    return dado

                linha_planilha = [
                    cnpj,
                    nome_empresarial,
                    aberturaCnpj,
                    periodoApuracao[-10:],
                    floatExcel(rpa[2]),
                    floatExcel(rbt12[2]),
                    floatExcel(simplesNacional),
                    floatExcel(inssCpp),
                    floatExcel(fopagTotal)
                ]               

                #
                #
                #
                #
                # Grava dados em um txt

                # Especifique o nome do arquivo de texto
                #raiz_cnpj = ''.join(filter(str.isdigit, cnpj))
                #arquivo_texto = f"Z:\\RPA\\Simples Nacional\\BD_Simples_Nacional\\{raiz_cnpj}.txt"

                # Texto que você deseja adicionar ao arquivo
                #texto_a_adicionar = '|'.join(linha_dado)
                
                # Verifica se o arquivo já existe
                #if not os.path.isfile(arquivo_texto):
                    # Se o arquivo não existir, cria um novo arquivo
                #    with open(arquivo_texto, 'w') as arquivo:
                #        arquivo.write(f"{texto_a_adicionar}\n")
                #else:
                    
                    # Lê o conteúdo atual do arquivo
                #    with open(arquivo_texto, 'r') as arquivo:
                #        linhas = arquivo.readlines()
                                        
                    # Verifica se a nova linha já existe no conteúdo
                #    ja_existe = False
                #    for i, linha in enumerate(linhas):
                #        if linha.strip().split('|')[5] == linha_dado[5]:  # Compara o período da declaração
                #            linhas[i] = texto_a_adicionar + '\n'
                #            ja_existe = True
                #            break
                
                    # Se a linha não existir, adiciona a nova linha ao conteúdo
                #    if not ja_existe:
                #        linhas.append(texto_a_adicionar + '\n')
                    
                    # Função para extrair a data do campo 6 (assumindo que o campo é uma string no formato "DD/MM/AAAA")
                #    def extrair_data(linha):
                #        campos = linha.strip().split('|')
                        
                #        if len(campos) > 5:
                #            data_str = campos[5]  # Assumindo que o campo 6 contém a data no formato "DD/MM/AAAA"
                #            try:
                #                data_obj = datetime.strptime(data_str, "%d/%m/%Y")
                #                return data_obj
                #            except ValueError:
                #                return None
                #        else:
                #            return None

                    # Ordenar as linhas com base nas datas
                #    linhas_ordenadas = sorted(linhas, key=extrair_data)
                    
                    # Salva o conteúdo atualizado de volta no arquivo
                #    with open(arquivo_texto, 'w') as arquivo:
                #        arquivo.writelines(linhas_ordenadas)
                
        planilha(linha_planilha)

        if anexoFatorR != "Anexo III":
            return ["Advertencia", "Simples nacional calculado no anexo V, verifique a declaração!"]
        
        return ['Processado com sucesso', arquivo_texto, {'valorFopag': fopagMinima, 'salarioMinimo': salarioMinimoPeriodo, 'empresa': nome_empresarial, 'cnpj': cnpj, 'periodoInicial': inicioMes, 'periodoFinal': periodoApuracao[-10:], 'valorSimples': floatExcel(simplesNacional), "issRetido": issRetido}]

    except Exception as e:
        
        return ['Erro ao tentar processar o documento', e]
    
leitorPgdasD("C:/Users/rodri/Downloads/PGDASD-DECLARACAO-50585877202311001.pdf")