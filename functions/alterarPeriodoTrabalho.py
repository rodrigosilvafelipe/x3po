from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions.functions import esperar_elemento_id
import time
import pyautogui

def definir_periodo_trabalho(driver, periodo):
    try:
        input_data = esperar_elemento_id(driver, "Conteudo_UserEmpresaPeriodoTrabalho_EditDataInicial")
        input_data.click()
        time.sleep(0.5)
        input_data.send_keys(periodo)
        input_data.send_keys(Keys.ENTER)
        # pyautogui.press('enter')
        time.sleep(1)
        return {"Execucao": True, "Mensagem": "Processo concluído com sucesso!"}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}