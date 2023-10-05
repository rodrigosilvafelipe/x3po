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

def baixarDarfRecibo(driver, razao_social):

    driver.get("https://www.makroweb.com.br/FormControleTributos/ImpostosDCTFWeb/ImpostosDCTFWeb.aspx")

    try:

        mover_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[3]/div[1]/div/table/tbody/tr/td[7]/span')

        mover_id(driver, 'Conteudo_GridImpostosDCTFWebPai_BtnSituacao_0')

        pularGerarDarf = False

        btn_gerarDarf = esperar_elemento_id(driver, "Conteudo_GridImpostosDCTFWebPai_BtnGerarDocArrecadacao_0")
        if btn_gerarDarf.get_attribute("disabled") is None:
            btn_gerarDarf.click()
            time.sleep(1)
            btn_confirmarGerarDarf = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
            btn_confirmarGerarDarf.click()
        else:
            pularGerarDarf = True

        modalMsgSistema(driver)

        driver.get("https://www.makroweb.com.br/FormControleTributos/ImpostosDCTFWeb/ImpostosDCTFWeb.aspx")

        mover_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[3]/div[1]/div/table/tbody/tr/td[7]/span')

        mover_id(driver, 'Conteudo_GridImpostosDCTFWebPai_BtnSituacao_0')

        pularGerarRecibo = False

        btn_gerarRecibo = esperar_elemento_id(driver, "Conteudo_GridImpostosDCTFWebPai_BtnConsultarDCTFWeb_0")
        if btn_gerarRecibo.get_attribute("disabled") is None:
            btn_gerarRecibo.click()
            time.sleep(1)
            btn_confirmarGerarRecibo = esperar_elemento_xpath(driver, '//*[@id="id_alertWindow"]/div[3]/input[1]')
            btn_confirmarGerarRecibo.click()
        else:
            pularGerarRecibo = True

        modalMsgSistema(driver)

        driver.get("https://www.makroweb.com.br/FormControleTributos/ImpostosDCTFWeb/ImpostosDCTFWeb.aspx")

        mover_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[3]/div[1]/div/table/tbody/tr/td[7]/span')

        mover_id(driver, 'Conteudo_GridImpostosDCTFWebPai_BtnSituacao_0')

        if pularGerarDarf == False:
            btn_imprimirDarf = esperar_elemento_id(driver, 'Conteudo_GridImpostosDCTFWebPai_SpBtnExibirArquivoArrecadacao_0')
            btn_imprimirDarf.click()
            time.sleep(1)
            embed_salvarDarf = esperar_elemento_id(driver,'EmbedArquivo')
            link = embed_salvarDarf.get_attribute("src")
            pdf = f"Darf-DCTFWeb-{razao_social}"
            baixar_pdf(driver, link, pdf, 1)
            time.sleep(1)
            btn_fecharSalvarDarf = esperar_elemento_xpath(driver,'//*[@id="modal_Master_Custom"]/div/div/div[1]/div/div/div[2]/button')
            btn_fecharSalvarDarf.click()

        mover_xpath(driver, '//*[@id="update_panel_Master_Conteudo"]/div/div[3]/div[1]/div/table/tbody/tr/td[7]/span')

        mover_id(driver, 'Conteudo_GridImpostosDCTFWebPai_BtnSituacao_0')

        if pularGerarRecibo == False:
            btn_imprimirRecibo = esperar_elemento_id(driver, 'Conteudo_GridImpostosDCTFWebPai_SpBtnExibirArquivoArrecadacao_0')
            btn_imprimirRecibo.click()
            time.sleep(1)
            embed_salvarRecibo = esperar_elemento_id(driver,'EmbedArquivo')
            link = embed_salvarRecibo.get_attribute("src")
            pdf = f"Recibo-DCTFWeb-{razao_social}"
            baixar_pdf(driver, link, pdf, 1)
            time.sleep(1)
            btn_fecharSalvarRecibo= esperar_elemento_xpath(driver,'//*[@id="modal_Master_Custom"]/div/div/div[1]/div/div/div[2]/button')
            btn_fecharSalvarRecibo.click()

        return {"Execucao": True, "Mensagem": "Processado com sucesso!"}

    except Exception as e:
        return {"Execucao": False, "Mensagem": e}
