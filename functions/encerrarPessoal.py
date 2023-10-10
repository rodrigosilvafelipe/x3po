from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath
from functions.modalMsgSistema import modalMsgSistema
import time
import pyautogui

def encerrar_pessoal(driver):

    driver.get("https://www.makroweb.com.br/FormPessoal/Encerramento/EncerramentoPessoal.aspx")

    try:
        btnValidar = esperar_elemento_id(driver, "Conteudo_BtnValidarDepartamento")
        btnValidar.click()
        time.sleep(2)
        modal = modalMsgSistema(driver)
        
        if modal["Execucao"] == False:
            return {"Execucao": False, "Mensagem": modal["Mensagem"]}
        
        driver.get("https://www.makroweb.com.br/FormPessoal/Encerramento/EncerramentoPessoal.aspx")
        
        btnValidar = esperar_elemento_id(driver, "Conteudo_BtnEncerrarDepartamento")
        btnValidar.click()

        btnConfirmar = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
        btnConfirmar.click()
        time.sleep(2)
        modal = modalMsgSistema(driver)
        
        if modal["Execucao"] == False:
            return {"Execucao": False, "Mensagem": modal["Mensagem"]}

        return {"Execucao": True, "Mensagem": "Execução completa"}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
