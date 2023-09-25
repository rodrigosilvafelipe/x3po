from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions.functions import esperar_elemento_id
import time
import pyautogui

def alterar_empresa(driver, razao_social):
    try:
        input_filtro = esperar_elemento_id(driver, "EditFiltroRazSocCabecalho")
        time.sleep(0.5)
        input_filtro.click()
        time.sleep(0.5)
        input_filtro.send_keys(razao_social)
        time.sleep(10)
        pyautogui.press("enter")
        time.sleep(1)
        return True

    except Exception as e:
        return False
