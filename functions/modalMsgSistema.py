from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_class
import time
import pyautogui

def modalMsgSistema(driver):
    i = 1
    for _ in range(60):
        
        try:
            modal = esperar_elemento_class(driver, "msistema-container")
            modalBody = modal.find_element(By.CLASS_NAME, "msistema-body")

            # Encontrar todas as divs com a classe "row" aninhadas dentro da div com a classe "msistema-body"
            myRows = modalBody.find_elements(By.CLASS_NAME, 'row')

            if len(myRows) > 0:
                
                validacao = False
                validacoes = []

                rows = modalBody.find_element(By.CLASS_NAME, 'row')

                # Percorrer cada div encontrada
                for row in myRows:
                    div1 = row.find_element(By.CLASS_NAME, 'itens-msistema')
                    div2 = div1.find_element(By.CLASS_NAME, 'div-texto')
                    msgValidacao = div2.find_elements(By.TAG_NAME, 'p')
                    isValidacao = msgValidacao[-1].text
                    if isValidacao == "Operação interrompida." or isValidacao == "Operação interrompida!":
                        texto = div2.find_element(By.TAG_NAME, 'p').text
                        validacoes.append(texto)
                        validacao = True
                
                if validacao is True:
                    return {"Execucao": False, "Mensagem": "<br><br>".join(validacoes)}
                return {"Execucao": True, "Mensagem": "Executado sem validacoes"}

        except Exception as e:
            pass
        
        time.sleep(1)

    raise Exception({"Execucao": False, "Mensagem": "Não foi possível manipular o modal após 60 segundos de espera."})
