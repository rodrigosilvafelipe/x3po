import os
import shutil
import time
import subprocess
import sys
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import platform

from leitorPgdasD import leitorPgdasD
from validadorReceitaBruta import validadorReceitaBruta

# Defina o caminho da pasta que você deseja monitorar
folder_to_watch = 'Z:\RPA\Simples Nacional\PGDAS-D a processar'

# Configurar o registro para o arquivo de log
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'observadorPgdasD.log')
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
                pdf_processing_thread = threading.Thread(target=process_pdf, args=(event.src_path,))
                pdf_processing_thread.start()

def process_pdf(pdf_path):
    
    processo = leitorPgdasD(pdf_path)

    # Especifique o caminho completo do arquivo PDF que você deseja mover
    pdf_path = pdf_path

    processamentoReceita = False
    
    if processo[0] == "Processado com sucesso":
        # validarReceita = validadorReceitaBruta(processo[1])
        # if validarReceita == 'Processado com sucesso':
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado"
        # processoCompleto = True
        #else:
        #    dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado com erro"
        #    processoCompleto = False
        #    logging.info(validarReceita)
    else:
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado com erro"
        logging.info(processo[0])
        logging.info(processo[1])

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
            print("Uso: python script.py --start")
    elif platform.system() == 'Linux':
        run_monitor()
    else:
        print("Sistema operacional nao suportado.")
