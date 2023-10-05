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

def gerarReciboPagto(driver, razao_social):

    # ######################## Inicio - Acessar página de relatórios #########################

    driver.get("https://www.makroweb.com.br/Relatorios.aspx?PkModulos=525")

    seletor = ".toast-place-right"  # Exemplo de seletor de classe
    driver.execute_script(f"document.querySelector('{seletor}').innerHTML = '';")

    # ######################## Fim - Acessar página de relatórios #########################
    #
    #
    #
    # ######################## Inicio - Gerar folha #########################
    try:

        vizualizar = esperar_elemento_id(driver, "Conteudo_GridRelatorios_BtnVisualizar_0")
        vizualizar.click()

        time.sleep(2)

        driver.switch_to.default_content()

        exibirDataVencimento = esperar_elemento_id(driver, "CkParametrosRelatorios_55")
        if not exibirDataVencimento.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[1]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        exibirProtocolo = esperar_elemento_id(driver, "CkParametrosRelatorios_67")
        if exibirProtocolo.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[2]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        exibirSomente1Via = esperar_elemento_id(driver, "CkParametrosRelatorios_68")
        if not exibirSomente1Via.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[3]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        exibirTomador = esperar_elemento_id(driver, "CkParametrosRelatorios_211")
        if exibirTomador.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[4]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        incluirEventosInformativos = esperar_elemento_id(driver, "CkParametrosRelatorios_189")
        if not incluirEventosInformativos.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[5]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        reducao13Salario = esperar_elemento_id(driver, "CkParametrosRelatorios_131")
        if not reducao13Salario.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[6]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        somenteReciboValores = esperar_elemento_id(driver, "CkParametrosRelatorios_256")
        if not somenteReciboValores.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[7]/span/span/label')
            for _ in range(60):
                if label.is_displayed() and label.is_enabled():
                    label.click()
                    break
                else:
                    time.sleep(1)

        time.sleep(1)

        tipoImpressao = esperar_elemento_xpath(driver, '//*[@id="0"]/td/div[3]/div/div[8]/div/select')
        seletor = Select(tipoImpressao)
        seletor.select_by_visible_text("Todos desta Empresa")
        time.sleep(0.5)

        embed_salvarDarf = esperar_elemento_id(driver, 'Conteudo_EmbedRelatorio')
        link = embed_salvarDarf.get_attribute("src")
        pdf = f"Recibo de pagamento de salário - {razao_social}"
        baixar_pdf(driver, link, pdf, 1)

        time.sleep(1)
        
        return {"Execucao": True, "Mensagem": "Processado com sucesso."}
    
    except Exception as e:
        
        return {"Execucao": False, "Mensagem": e}
