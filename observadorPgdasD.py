import os
import shutil
import time
import sys
import logging
import threading
import platform
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from leitorPgdasD import leitorPgdasD
from functions.enviarEmail import enviarEmail
from functions.alterarPeriodoTrabalho import definir_periodo_trabalho as periodoTrabalho
from functions.alterarEmpresa import alterar_empresa
from acessarMakro import fazer_login_makro
from functions.gerarRelatorioRelacaoEmpregados import gerarRelatorioRelacaoEmpregados
from functions.fecharToasts import fecharToast
from functions.renomearRelatorioDadosEmpregados import renomearRelatorio
from functions.extratorDadosRelacaoEmpregados import dadosRelacaoEmpregados
from functions.processaDados import processaDados
from functions.limparPasta import limparPasta
from functions.alterarProLabore import alterar_prolabore
from functions.gerarFopag import gerar_fopag
from functions.gerarPeriodicosESocial import gerar_periodicos

# Defina o caminho da pasta que você deseja monitorar
folder_to_watch = 'Z:\RPA\Simples Nacional\PGDAS-D a processar'

# Obtém o diretório onde o arquivo .exe está localizado
exe_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Caminho absoluto para o arquivo de log
log_file = os.path.join(exe_dir, 'observadorPgdasD.log')

# Configuração do registro
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Crie um semáforo para controlar o acesso concorrente
thread_semaphore = threading.Semaphore(1)

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        time.sleep(2)
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            logging.info(f"PDF detectado: {event.src_path}")

            # Adquire o semáforo antes de iniciar a nova thread
            thread_semaphore.acquire()

            def thread_target():
                try:
                    process_pdf(event.src_path)
                finally:
                    # Libera o semáforo quando a thread terminar
                    thread_semaphore.release()

             # Inicia um thread para processar o PDF
            pdf_processing_thread = threading.Thread(target=thread_target)
            pdf_processing_thread.start()

def acessar_makro(info):
    logging.info("Acessando Makro")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "Z:\RPA\Folha Pró-Labore\Fopag Processada\\",
        "download.prompt_for_download": False,  # Para não mostrar a caixa de diálogo de download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False  # Para não verificar downloads com segurança
    })

    # Inicialize o webdriver do Selenium (certifique-se de ter o ChromeDriver instalado e no PATH)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    usuario = "X3PO"
    senha = "Escritax@X3PO"
    try:
        fazer_login_makro(driver, usuario, senha)
        periodoTrabalho(driver, info['periodoInicial'])
        alterar_empresa(driver, info['empresa'])
        exec = gerarRelatorioRelacaoEmpregados(driver, info)
        if exec['Execucao'] == False:
            configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Não foi possível gerar o relatório de relação de empregados na empresa {info['empresa']}\n{exec['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        renomearRelatorio("Z:\\RPA\\Folha Pró-Labore\\Fopag Processada\\", info['empresa'])
        arquivo = f"Z:\\RPA\\Folha Pró-Labore\\Fopag Processada\\{info['empresa']}.xlsx"
        time.sleep(1)
        dados = dadosRelacaoEmpregados(arquivo)
        if dados['execução'] == False:
            limparPasta("Z:\RPA\Folha Pró-Labore\Fopag Processada")
            configEmail = {
                'assunto': "Erro ao processar relação de empregados",
                'mensagem': f"Não foi possível extrair os dados do relatório de relação de empregados na empresa {info['empresa']}\n{dados['mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return

        socios = processaDados(dados["dados"], info['valorFopag'], info['salarioMinimo'])
        os.remove(arquivo)
        for item in socios['dados']:
            if item['proLabore'] != item['anterior']:
                alterarProLabore = alterar_prolabore(driver, item['nomeSocio'], info['periodoInicial'], item['proLabore'])
                if alterarProLabore["Execucao"] == False:
                    configEmail = {
                        'assunto': "Erro ao alterar pró-labore",
                        'mensagem': f"Não foi possível alterar o pró-labore na empresa {info['empresa']}<br><br>{alterarProLabore['Mensagem']}"
                    }
                    enviarEmail(configEmail)
                    driver.quit()
                    return

        gerarFolha = gerar_fopag(driver)

        if gerarFolha["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar folha de pagamento",
                'mensagem': f"Não foi possível gerar a folha de pagamento na empresa {info['empresa']}<br><br>{gerarFolha['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        gerarPeriodicos = gerar_periodicos(driver)
        if gerarPeriodicos["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar periodicos do e-Social",
                'mensagem': f"Não foi possível gerar os eventos periódicos do e-social na empresa {info['empresa']}<br><br>{gerarFolha['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return

        time.sleep(1)
        driver.quit()
    except Exception as e:
        logging.info(e)

def process_pdf(pdf_path):
    # arquivoStart = "Z:\RPA\Simples Nacional\PGDAS-D a processar\processando.txt"
    # for _ in range(3600):
        
    #     if os.path.isfile(arquivoStart):
    #         time.sleep(1)
    #     else:                    
    #         with open(arquivoStart, 'w') as arquivo:
    #             arquivo.write("Processando...")
    #         break
    
    processo = leitorPgdasD(pdf_path)

    # Especifique o caminho completo do arquivo PDF que você deseja mover
    pdf_path = pdf_path
    
    if processo[0] == "Processado com sucesso":
        
        logging.info(f"Documento processado com sucesso.")
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado"
        info = processo[2]

        acessar_makro(info)

    else:
        logging.info(processo[0])
        logging.info(processo[1])
        configEmail = {
            'assunto': "Erro ao processar declaração do simples nacional",
            'mensagem': f"{processo[1]}\n",
            'pdf64': pdf_path,
            'nomeDocumento': os.path.basename(pdf_path)
        }
        
        logging.info("Enviando email com detalhaes.")
        email = enviarEmail(configEmail)
     
        if email['execução'] == False:
            logging.info("Não foi possível enviar o e-mail.")
        else:
            logging.info("Email enviado")
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado com erro"

    # Verifique se o arquivo PDF existe antes de mover
    if os.path.exists(pdf_path):
        # Verifique se o diretório de destino existe, crie-o se não existir
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        # Construa o caminho completo de destino
        dest_path = os.path.join(dest_directory, os.path.basename(pdf_path))

        # Verifica se o arquivo já existe
        if os.path.isfile(dest_path):
            # Se o arquivo existir no destino, exclua-o
            os.remove(dest_path)

        # Mova o arquivo PDF para o diretório de destino
        shutil.move(pdf_path, dest_path)
        logging.info(f"Arquivo PDF movido para {dest_path}")
    else:
        logging.info("O arquivo PDF especificado nao existe.")
    
    # os.remove(arquivoStart)


def run_monitor():
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    logging.info(f"Iniciando monitoramento de {folder_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        if len(sys.argv) == 2 and sys.argv[1] == "--start":
            run_monitor()
        else:
            print("Uso: python observadorPgdasD.py --start")
    elif platform.system() == 'Linux':
        run_monitor()
    else:
        print("Sistema operacional nao suportado.")
