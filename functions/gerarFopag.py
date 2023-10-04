from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.modalMsgSistema import modalMsgSistema
import time
import pyautogui

def gerar_fopag(driver):

    driver.get("https://www.makroweb.com.br/FormPessoal/FolhaPagamento/Recibo/MovPessoal.aspx")

    try:
        time.sleep(1)
        gerar_folha = esperar_elemento_id(driver, "Conteudo_UserGeracaoPessoal1_BtnGerar")
        gerar_folha.click()
        time.sleep(1)
        select = esperar_elemento_id(driver, "Conteudo_UserGeracaoPessoal1_EditTipoGeraFolha")
        selectGerarPor = Select(select)
        selectGerarPor.select_by_visible_text("Todos os Empregados")
        time.sleep(0.5)
        btnGerar = esperar_elemento_id(driver, "BtnConfirmaGeracao")
        btnGerar.click()
        modal = modalMsgSistema(driver)
        if modal["Execucao"] == False:
            return {"Execucao": False, "Mensagem": modal["Mensagem"]}
        
        return {"Execucao": True, "Mensagem": modal["Mensagem"]}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
