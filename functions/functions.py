import time
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywinauto import Application

def esperar_elemento_id(driver, id_elemento, tempo_maximo_espera=60):
    for _ in range(tempo_maximo_espera):
        try:
            elemento = driver.find_element(By.ID, id_elemento)
            if elemento:
                return elemento
        except Exception as e:
            # Elemento não encontrado, aguarde 1 segundo e tente novamente
            pass

        time.sleep(1)  # Aguarde 1 segundo entre as tentativas

    # Se o loop for concluído sem encontrar o elemento
    raise Exception(f"Elemento id '{id_elemento}' não encontrado após {tempo_maximo_espera} segundos")

def esperar_elemento_xpath(driver, xpath_elemento, tempo_maximo_espera=60):
    for _ in range(tempo_maximo_espera):
        try:
            elemento = driver.find_element(By.XPATH, xpath_elemento)
            if elemento:
                # elemento = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, xpath_elemento))
                # )
                return elemento
        except Exception as e:
            # Elemento não encontrado, aguarde 1 segundo e tente novamente
            pass

        time.sleep(1)  # Aguarde 1 segundo entre as tentativas

    # Se o loop for concluído sem encontrar o elemento
    raise Exception(f"Elemento xpath '{xpath_elemento}' não encontrado após {tempo_maximo_espera} segundos")

def esperar_elemento_tag(driver, tag_elemento, tempo_maximo_espera=60):
    for _ in range(tempo_maximo_espera):
        try:
            elemento = driver.find_element(By.TAG_NAME, tag_elemento)
            if elemento:
                # elemento = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, xpath_elemento))
                # )
                return elemento
        except Exception as e:
            # Elemento não encontrado, aguarde 1 segundo e tente novamente
            pass

        time.sleep(1)  # Aguarde 1 segundo entre as tentativas

    # Se o loop for concluído sem encontrar o elemento
    raise Exception(f"Elemento xpath '{tag_elemento}' não encontrado após {tempo_maximo_espera} segundos")

def esperar_elemento_class(driver, classe_elemento, tempo_maximo_espera=60):
    for _ in range(tempo_maximo_espera):
        try:
            elemento = driver.find_element(By.CLASS_NAME, classe_elemento)
            if elemento:
                # elemento = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, xpath_elemento))
                # )
                return elemento
        except Exception as e:
            # Elemento não encontrado, aguarde 1 segundo e tente novamente
            pass

        time.sleep(1)  # Aguarde 1 segundo entre as tentativas

    # Se o loop for concluído sem encontrar o elemento
    raise Exception(f"Elemento xpath '{classe_elemento}' não encontrado após {tempo_maximo_espera} segundos")

def clicar(elemento):
    for _ in range(60):
        try:
            if elemento.is_displayed() and elemento.is_enabled():
                elemento.click()
                time.sleep(0.5)
                return True
            else:
                time.sleep(1)
        except Exception as e:
            return False

    raise Exception(False)

def baixar_pdf(driver, url, documento, pause=10):
    script_js = f"""
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "{url}", true);
                xhr.responseType = "blob";

                xhr.onload = function () {{
                  if (xhr.status === 200) {{
                    var blob = xhr.response;
                    var nomeArquivo = "{documento}.pdf"; // Nome que você deseja dar ao arquivo
                    var link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = nomeArquivo;
                    link.style.display = "none";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                  }}
                }};

                xhr.send();
                            """

    pdf_data = driver.execute_script(script_js)
    # time.sleep(pause)
    # pyautogui.write(documento)
    # pyautogui.press("enter")