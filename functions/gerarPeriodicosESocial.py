from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath
from functions.modalMsgSistema import modalMsgSistema
import time
import pyautogui

def gerar_periodicos(driver):

    driver.get("https://www.makroweb.com.br/FormPessoal/eSocial/DadosPeriodicos/eSocialDadosPeriodicos.aspx")

    try:
        time.sleep(1)
        gerar_dados = esperar_elemento_id(driver, "Conteudo_BtnGerar")
        gerar_dados.click()
        time.sleep(1)
        btnSim = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
        btnSim.click()
        modal = modalMsgSistema(driver)
        if modal["Execucao"] == False:
            return {"Execucao": False, "Mensagem": modal["Mensagem"]}
        
        return {"Execucao": True, "Mensagem": modal["Mensagem"]}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
