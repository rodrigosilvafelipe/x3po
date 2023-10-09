from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from functions.functions import esperar_elemento_id
from functions.functions import esperar_elemento_xpath
from functions.modalMsgSistema import modalMsgSistema
from functions.functions import baixar_pdf
import time
import pyautogui

def mover_xpath(driver, xpath):
    try:
        tabela = esperar_elemento_xpath(driver, xpath, 10)
        actions = ActionChains(driver)
        actions.move_to_element(tabela).perform()
        time.sleep(0.5)
        return True
    except Exception as e:
        return False
    
def mover_id(driver, id):
    try:
        tabela = esperar_elemento_id(driver, id, 10)
        actions = ActionChains(driver)
        actions.move_to_element(tabela).perform()
        time.sleep(0.5)
        return True
    except Exception as e:
        return False

def emitirDas(driver, razao_social):

    driver.get("https://www.makroweb.com.br/FormControleTributos/Impostos/Impostos.aspx")

    try:

        mover_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[3]/div[1]/div/table/tbody/tr[1]/td[10]/span')

        # Encontre a tabela pelo ID
        tabela = esperar_elemento_id(driver, "Conteudo_GridImpostos")

        # Percorra cada linha da tabela
        for linha in tabela.find_elements(By.TAG_NAME, "tr"):
            
            # Encontre a décima célula
            celula = linha.find_elements(By.TAG_NAME, "td")[9]
            
            # Verifique se existe uma div com a classe 'row'
            div_row = celula.find_element(By.CLASS_NAME, "row")
            
            # Verifique se existe uma div com a classe 'text-truncate' dentro da div 'row'
            div_truncate = div_row.find_element(By.CLASS_NAME, "text-truncate")
            
            # Verifique se o texto da tag 'a' é o desejado
            if div_truncate.find_element(By.TAG_NAME, "a").text == "0016 - DAS - Doc de Arrecadação do Simples Nacional":
                actions = ActionChains(driver)
                actions.move_to_element(div_truncate).perform()
                time.sleep(0.5)
                div_btn = div_row.find_element(By.CLASS_NAME, "group-buttons-grid")
                span = div_btn.find_elements(By.TAG_NAME, "span")[3]
                input_elements = span.find_elements(By.TAG_NAME, "input")
                if len(input_elements) > 0:
                    span.click()
                else:
                    gerarDas = div_btn.find_elements(By.TAG_NAME, "span")[1]
                    gerarDas.click()
                    time.sleep(1)
                    confirmar = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
                    confirmar.click()
                
                for _ in range(60):
                    try:
                        embed_salvarDarf = esperar_elemento_id(driver,'EmbedImpostos')
                        link = embed_salvarDarf.get_attribute("src")
                        if link:
                            pdf = f"Das-Simples-Nacional-{razao_social}"
                            baixar_pdf(driver, link, pdf, 1)
                            break
                    except Exception as e:
                        time.sleep(1)
                        pass

                # btn_fecharSalvarDarf = esperar_elemento_xpath(driver,'//*[@id="modal_Master_Custom"]/div/div/div[1]/div/div/div[2]/button')
                # btn_fecharSalvarDarf.click()

        return {"Execucao": True, "Mensagem": "Processado com sucesso!"}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
