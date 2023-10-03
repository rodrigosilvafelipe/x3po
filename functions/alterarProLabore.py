from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
import time
import pyautogui

def alterar_prolabore(driver, socio, data, proLabore):

    driver.get("https://www.makroweb.com.br/FormPessoal/Empregados/CadSalarios/CadSalarios.aspx")

    try:
        input_filtro = esperar_elemento_id(driver, "Conteudo_Empregados1_EditDescricao")
        time.sleep(0.5)
        input_filtro.click()
        time.sleep(0.5)
        input_filtro.send_keys(socio)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        btnIncluirNovo = esperar_elemento_id(driver, "Conteudo_BtnIncluir")
        btnIncluirNovo.click()
        time.sleep(1)
        dataInicial = esperar_elemento_id(driver, "Conteudo_EditDataInicial")
        dataInicial.send_keys(data)
        time.sleep(2)
        referencia = esperar_elemento_id(driver, "Conteudo_EditReferencia")
        referencia.click()
        referencia.send_keys('30')
        time.sleep(2)
        valorSalario = esperar_elemento_id(driver, "Conteudo_EditSalario")
        valorSalario.click()
        valorSalario.send_keys(int(proLabore))
        time.sleep(2)
        tabMotivo = esperar_elemento_id(driver, "tab_motivo")
        tabMotivo.click()
        time.sleep(1)
        motivo = esperar_elemento_id(driver, "Conteudo_EditMotivoAumento")
        selectMotivo = Select(motivo)
        selectMotivo.select_by_visible_text("Espontâneo")
        pyautogui.press("enter")
        time.sleep(4)
        return True

    except Exception as e:
        return False
