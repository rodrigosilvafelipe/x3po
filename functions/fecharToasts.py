from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions.functions import esperar_elemento_class
from functions.functions import clicar
import time
import pyautogui

def fecharToast(driver):
    divToasts = esperar_elemento_class(driver, "toast-place-right")
    toasts = divToasts.find_element(By.CLASS_NAME, "toast")

    for toast in toasts:
        try:
            # Encontrar o botão de fechar dentro do toast e clicar nele
            close_button = toast.find_element(By.CLASS_NAME, 'toast-close')
            clicar(close_button)
            time.sleep(1)
        except Exception as e:
            return f'Erro ao fechar toast: {e}'