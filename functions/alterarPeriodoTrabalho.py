from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.functions import esperar_elemento_id
import time
import pyautogui

def definir_periodo_trabalho(driver, periodo):
    try:
        input_data = esperar_elemento_id(driver, "Conteudo_UserEmpresaPeriodoTrabalho_EditDataInicial")
        input_data.click()
        time.sleep(0.5)
        input_data.send_keys(periodo)
        pyautogui.press('enter')
        time.sleep(1)
        return True

    except Exception as e:
        return False