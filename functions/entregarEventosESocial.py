from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath
from functions.modalMsgSistema import modalMsgSistema
import time
import pyautogui

def entregar_eventos(driver):

    driver.get("https://www.makroweb.com.br/FormPessoal/eSocial/eSocial.aspx")

    try:
        filtro = esperar_elemento_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/a')
        filtro.click()

        time.sleep(1)

        proc_advertencia = esperar_elemento_id(driver, 'Conteudo_CkFiltroProcessadoAdvertencias')
        if proc_advertencia.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="Conteudo_Panel6"]/div[2]/span/span/label')
            label.click()
        
        time.sleep(0.5)

        proc_sucesso = esperar_elemento_id(driver, 'Conteudo_CkFiltroProcessado')
        if proc_sucesso.get_attribute("checked"):
            label = esperar_elemento_xpath(driver, '//*[@id="Conteudo_Panel6"]/div[4]/span/span/label')
            label.click()

        time.sleep(0.5)

        fechar_filtro = esperar_elemento_xpath(driver, '//*[@id="Conteudo_UpdatePanel2"]/div[1]/div/div[2]/button')
        fechar_filtro.click()

        time.sleep(2)

        qtd_eventos = 1
        tentativas = 5

        while qtd_eventos > 0:

            tabela = esperar_elemento_id(driver, 'Conteudo_GrideSocial')
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')
            if len(linhas) > 1:
                qtd_eventos = len(linhas)
            else:
                celulas = linhas[0].find_elements(By.TAG_NAME, 'td')
                existe_evento = len(celulas)
                if existe_evento > 1:
                    qtd_eventos = 1
                else:
                    qtd_eventos = 0

            if qtd_eventos > 0:

                liberar_eventos = esperar_elemento_id(driver, 'Conteudo_CkLiberaEnvioTodastarefas')
                if not liberar_eventos.get_attribute("checked"):
                    label = esperar_elemento_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/span/label')
                    label.click()

                time.sleep(1)

                enviar_eventos = esperar_elemento_id(driver,'Conteudo_LnkEnviareSocialFiltroCorrente')
                enviar_eventos.click()

                time.sleep(1)

                confirmar = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
                confirmar.click()

                time.sleep(5)

                driver.get("https://www.makroweb.com.br/FormPessoal/eSocial/eSocial.aspx")

                tabela = esperar_elemento_id(driver, 'Conteudo_GrideSocial')
                linhas = tabela.find_elements(By.TAG_NAME, 'tr')
                if len(linhas) > 1:
                    qtd_eventos_verifica = len(linhas)
                else:
                    celulas = linhas[0].find_elements(By.TAG_NAME, 'td')
                    existe_evento = len(celulas)
                    if existe_evento > 1:
                        qtd_eventos_verifica = 1
                    else:
                        qtd_eventos_verifica = 0

                if qtd_eventos_verifica == qtd_eventos:
                    tentativas -= 1

                if tentativas == 0:
                    qtd_eventos = 0

        return {"Execucao": True, "Mensagem": "Processado com sucesso!"}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
