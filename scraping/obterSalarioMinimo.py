from bs4 import BeautifulSoup
import requests
import json
import os
from datetime import datetime

def obterSalarioMinimo():
    try:
        cacheSalrioMinimo = "Z:\\RPA\\Folha Pró-Labore\\Salário Mínimo\\Consulta Salario Minimo.json"

        url = 'http://www.ipeadata.gov.br/exibeserie.aspx?stub=1&serid1739471028=1739471028'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        tabela = soup.find('table', {'id': 'grd_DXMainTable'})

        dados = []

        dataConsulta = datetime.now()
        dataConsulta = dataConsulta.strftime("%d/%m/%Y %H:%M:%S")

        consulta = {'consulta': dataConsulta}

        dados.append(consulta)

        linhas = tabela.find_all('tr')[1:]

        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) == 2:  # Certifique-se de que a linha tem 2 colunas (período e valor)
                data = colunas[0].get_text()
                data = data.split(".")
                if len(data) > 1:

                    if float(data[0]) > 2015:
                    
                        dataFormatada = f"{data[1]}/{data[0]}"
                    
                        obj = {
                            'periodo': dataFormatada,
                            'salario': colunas[1].get_text()
                        }
                    
                        dados.append(obj)

        # json_string = json.dumps(dados)

        if os.path.exists(cacheSalrioMinimo):
            # Se o arquivo existir, abra-o no modo de escrita para substituir o conteúdo
            with open(cacheSalrioMinimo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
        else:
            # Se o arquivo não existir, crie um novo arquivo e escreva o conteúdo nele
            with open(cacheSalrioMinimo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)

    except Exception as e:
        return e