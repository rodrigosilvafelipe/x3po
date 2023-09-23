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
from acessarMakro import fazer_login_makro

# Defina o caminho da pasta que você deseja monitorar
folder_to_watch = 'Z:\RPA\Simples Nacional\PGDAS-D a processar'

# Obtém o diretório onde o arquivo .exe está localizado
exe_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Caminho absoluto para o arquivo de log
log_file = os.path.join(exe_dir, 'observadorPgdasD.log')

# Configuração do registro
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Crie um semáforo para controlar o acesso concorrente
thread_semaphore = threading.Semaphore()

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            logging.info(f"PDF detectado: {event.src_path}")
            # Use o semáforo para adquirir um bloqueio antes de iniciar a thread
            with thread_semaphore:
                # Iniciar um thread para processar o PDF
                time.sleep(2)
                logging.info("Processo iniciado")
                pdf_processing_thread = threading.Thread(target=process_pdf, args=(event.src_path,))
                pdf_processing_thread.start()

def acessar_makro():
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
        time.sleep(10)
        driver.quit()
    except Exception as e:
        logging.info(e)

def process_pdf(pdf_path):
    
    processo = leitorPgdasD(pdf_path)

    # Especifique o caminho completo do arquivo PDF que você deseja mover
    pdf_path = pdf_path
    
    if processo[0] == "Processado com sucesso":
        
        logging.info(f"Documento processado com sucesso")
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado"

        acessar_makro()

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
