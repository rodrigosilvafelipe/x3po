import sys
import time
import os
import datetime
import pandas as pd
import pyautogui
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath

def gerarRelatorioRelacaoEmpregados(driver, opcoes):

    with open("Z:\RPA\mapa.json", 'r') as arquivo_json:
        # Leia o conteúdo do arquivo JSON
        mapa = json.load(arquivo_json)

    url = mapa["relatorios"]["modulo_145"]["url"]
    btnVisualizar = mapa["relatorios"]["modulo_145"]["Relacao de Empregados"]["id_btnVisualizar"]
    btnExcel = mapa["relatorios"]["modulo_145"]["Relacao de Empregados"]["id_btnExcel"]

    # ######################## Inicio - Acessar página de relatórios #########################

    driver.get(url)

    seletor = ".toast-place-right"  # Exemplo de seletor de classe
    driver.execute_script(f"document.querySelector('{seletor}').innerHTML = '';")

    # ######################## Fim - Acessar página de relatórios #########################
    #
    #
    #
    # ######################## Inicio - Gerar folha #########################
    try:

        servico = esperar_elemento_id(driver, "ImgPessoal")
        statusServico = servico.get_attribute("src")
        statusServico = statusServico.split("/")
        statusServico = statusServico[-1]
        if statusServico == "pessoal-cinza.svg":
            return {"Execucao": False, "Mensagem": "Servico modulo pessoal nao aplicado."}
        if statusServico == "pessoal-verde.svg":
            return {"Execucao": False, "Mensagem": "Servico modulo pessoal já foi encerrado."}

        vizualizar = esperar_elemento_id(driver, btnVisualizar)
        vizualizar.click()

        time.sleep(2)

        driver.switch_to.default_content()

        exportarExcel = esperar_elemento_id(driver, btnExcel)
        exportarExcel.click()

        time.sleep(2)

        clicarTela = esperar_elemento_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[1]/div[1]/div[1]/nav/ol/li')
        clicarTela.click()

        return {"Execucao": True, "Mensagem": "Processado com sucesso."}
    
    except Exception as e:
        
        return {"Execucao": False, "Mensagem": e}
