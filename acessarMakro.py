from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.functions import esperar_elemento_id
import time

def fazer_login_makro(driver, usuario_makro, senha_makro):

    try:
        # Acessar a url de login
        driver.get("https://www.makroweb.com.br/Login.aspx")
        # logger.info('Pagina de login acessada - https://www.makroweb.com.br/Login.aspx')

        # Preencher o campo Usuário
        usuario_input = esperar_elemento_id(driver, "EditUsuario")
        usuario_input.send_keys(usuario_makro)

        # Preencher o campo Senha
        senha_input = esperar_elemento_id(driver, "EditSenha")
        senha_input.send_keys(senha_makro)

        # Preencher o campo Escritório
        dominio_input = esperar_elemento_id(driver, "EditNomeDominio")
        dominio_input.send_keys("Escritax")

        # 5: Clicar no botão Login
        login_button = esperar_elemento_id(driver, "BtnLogin")
        for _ in range(60):
            if login_button.is_displayed() and login_button.is_enabled():
                login_button.click()
                break
            else:
                # logger.info("Aguardando modal para continuar")
                time.sleep(1)

        time.sleep(2)

        # Acessar o diário
        driver.get("https://www.makroweb.com.br/FormAgenda/Diario.aspx")

        time.sleep(2)

        return {"Execucao": True, "Mensagem": "Login efetuado com sucesso!"}

    except Exception as e:
        # logger.error(str(e))
        return {"Execucao": False, "Mensagem": e}