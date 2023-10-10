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
from functions.functions import baixar_pdf

def obterValor(driver):

    # ######################## Inicio - Acessar página de relatórios #########################

    driver.get("https://www.makroweb.com.br/FormPessoal/FolhaPagamento/Resumo/FolhaResumo.aspx")

    time.sleep(1)
    
    # ######################## Fim - Acessar página de relatórios #########################
    #
    #
    #
    # ######################## Inicio - Gerar folha #########################
    try:

        valor = esperar_elemento_id(driver, "Conteudo_LbRendimento")
        totalA = valor.text
        totalB = totalA.replace(".", "")
        totalB = totalB.replace(",", ".")
        totalC = float(totalB)
        
        return {"Execucao": True, "Mensagem": totalC}
    
    except Exception as e:
        
        return {"Execucao": False, "Mensagem": e}
