import sys
import time
import os
import datetime
import pandas as pd
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath

def gerarRelatorioRelacaoEmpregados(driver, opcoes):

    # ######################## Inicio - Acessar página de relatórios #########################

    driver.get("https://www.makroweb.com.br/Relatorios.aspx?PkModulos=145")

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

        vizualizar = esperar_elemento_id(driver, "Conteudo_GridRelatorios_BtnVisualizar_61")
        vizualizar.click()

        time.sleep(2)

        driver.switch_to.default_content()

        exportarExcel = esperar_elemento_id(driver, "Conteudo_GridRelatorios_BtnExcel_61")
        exportarExcel.click()

        time.sleep(2)

        clicarTela = esperar_elemento_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[1]/div[1]/div[1]/nav/ol/li')
        clicarTela.click()

        return {"Execucao": True, "Mensagem": "Processado com sucesso."}
    
    except Exception as e:
        
        return {"Execucao": False, "Mensagem": e}
