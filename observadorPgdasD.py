import os
import shutil
import time
import sys
import logging
import threading
import platform
import locale
import datetime
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
from functions.gerarReciboPagto import gerarReciboPagto
from functions.gerarPeriodicosESocial import gerar_periodicos
from functions.entregarEventosESocial import entregar_eventos
from functions.encerrarPessoal import encerrar_pessoal
from functions.darfReciboDctfWeb import baixarDarfRecibo
from functions.moverArquivos import mover_arquivos
from functions.emitirDas import emitirDas
from functions.zohoSheet import outrosVinculos
from functions.revisarVlrFopag import obterValor
from functions.inserirLinhaPlanilha import atualizar_valor_fopag

def converter_para_brl(valor):
    # Define o locale para pt_BR (Português Brasil)
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Converte o valor float para o formato de moeda BRL
    valor_formatado = locale.currency(valor, grouping=True)
    return valor_formatado

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

    validarOutrosVinculos = outrosVinculos(info['empresa'])
    if validarOutrosVinculos['Execucao'] == False:
        configEmail = {
            'assunto': "Não foi possível pesquisar dados na planilha de outros vínculos",
            'mensagem': f"Passo - Validar outros vínculos.<br><br>Não foi possível pesquisa dados na planilha de outros vínculos no processo da empresa {info['empresa']}<br><br>{validarOutrosVinculos['Erro']}"
        }
        enviarEmail(configEmail)
        return
    
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
        limparPasta("Z:\\RPA\\Folha Pró-Labore\\Fopag Processada")
        login= fazer_login_makro(driver, usuario, senha)
        if login['Execucao'] == False:
            configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Passo - Fazer login no Makro.<br><br>Não foi possível fazer login no Makro no processo da empresa {info['empresa']}<br><br>{login['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        periodo = periodoTrabalho(driver, info['periodoInicial'])
        if periodo['Execucao'] == False:
            configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Passo - Alterar período de trabalho no Makro.<br><br>Não foi possível alterar o periodo de trabalho no Makro no processo da empresa {info['empresa']}<br><br>{periodo['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        alterarEmpresa = alterar_empresa(driver, info['empresa'])
        if alterarEmpresa['Execucao'] == False:
            configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Passo - Alterar empresa no Makro.<br><br>Não foi possível alterar a empresa no Makro no processo da empresa {info['empresa']}<br><br>{alterarEmpresa['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        exec = gerarRelatorioRelacaoEmpregados(driver, info)
        if exec['Execucao'] == False:
            if(exec['Mensagem'] == 'Servico modulo pessoal nao aplicado.') and info['valorSimples'] != 0:

                configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Passo - Validar empresa com faturamento sem folha de pagamento.<br><br>A empresa {info['empresa']} possui faturamento e não está movimentando a folha de pagamento.<br><br>Verifique essa situação.<br><br>{exec['Mensagem']}"
                }
                enviarEmail(configEmail)
                driver.quit()
                return        

            if exec['Mensagem'] == 'Servico modulo pessoal já foi encerrado.' or exec['Mensagem'] == 'Servico modulo pessoal nao aplicado.':
                driver.quit()
                return

            configEmail = {
                'assunto': "Processo de folha automatizada cancelado.",
                'mensagem': f"Passo - Gerar ralatório relação de empregados.<br><br>Não foi possível gerar o relatório de relação de empregados na empresa {info['empresa']}<br><br>{exec['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        renomearRelatorio("Z:\\RPA\\Folha Pró-Labore\\Fopag Processada\\", info['empresa'])
        arquivo = f"Z:\\RPA\\Folha Pró-Labore\\Fopag Processada\\{info['empresa']}.xlsx"
        time.sleep(1)
        dados = dadosRelacaoEmpregados(arquivo, info['cnpj'])

        if dados['execução'] == False:
            limparPasta("Z:\RPA\Folha Pró-Labore\Fopag Processada")
            configEmail = {
                'assunto': "Erro ao processar relação de empregados",
                'mensagem': f"Passo - Extrair dados do relatório de empregados.<br><br>Não foi possível extrair os dados do relatório de relação de empregados na empresa {info['empresa']}<br><br>{dados['mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return

        socios = processaDados(dados["dados"], info['valorFopag'], info['salarioMinimo'])

        if socios['erro'] == True:
            configEmail = {
                        'assunto': "Não existem sócios com pró-labore",
                        'mensagem': f"Passo - Processar dados da relação de empregados.<br><br>Não foram encontrados sócios com pró-labore na empresa {info['empresa']}"
                    }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        os.remove(arquivo)

        if validarOutrosVinculos['Mensagem'] == False:
            
            textoSociosEmail = "<br><br>Seguem os valores do pró-labore dos sócios:<br><br>"
            for item in socios['dados']:
                textoSociosEmail += f"{item['nomeSocio']}: {converter_para_brl(item['proLabore'])}<br>"

            configEmail = {
                'assunto': f"Sócios possuem outros vínculos na empresa {info['empresa']}",
                'mensagem': f"Passo - Validar empresa com sócios que possuem outros vínculos.<br><br>A empresa {info['empresa']} existe na planilha de controle de empresas que possuem sócios com outros vínculos, por isso, o processo foi interrompido.<br><br>Execute a tarefa de forma manual.{textoSociosEmail}"
            }

            enviarEmail(configEmail)
            driver.quit()
            return
        
        valorX3po = 0
        
        for item in socios['dados']:
            valorX3po += item['proLabore']
            if item['proLabore'] != item['anterior']:
                alterarProLabore = alterar_prolabore(driver, item['nomeSocio'], info['periodoInicial'], item['proLabore'])
                if alterarProLabore["Execucao"] == False:
                    configEmail = {
                        'assunto': "Erro ao alterar pró-labore",
                        'mensagem': f"Passo - Alterar pró-labore.<br><br>Não foi possível alterar o pró-labore na empresa {info['empresa']}<br><br>{alterarProLabore['Mensagem']}"
                    }
                    enviarEmail(configEmail)
                    driver.quit()
                    return

        gerarFolha = gerar_fopag(driver)

        if gerarFolha["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar folha de pagamento",
                'mensagem': f"Passo - Gerar a folha de pagamento.<br><br>Não foi possível gerar a folha de pagamento na empresa {info['empresa']}<br><br>{gerarFolha['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        revisarValor = obterValor(driver)
        if revisarValor['Execucao'] == False:
            configEmail = {
                'assunto': "Erro ao validar valor da folha de pagamento",
                'mensagem': f"Passo - Validar o valor da folha de pagamento.<br><br>Não foi possível validar o valor da folha de pagamento na empresa {info['empresa']}<br><br>{revisarValor['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        valorMakro = revisarValor['Mensagem']
        valorX3po = float(valorX3po)

        if not abs(valorMakro - valorX3po) <= 2.0:
            configEmail = {
                'assunto': "O valor da folha de pagamento pode estar incorreto",
                'mensagem': f"Passo - Validar o valor da folha de pagamento.<br><br>Diferença no valor da folha de pagamento na empresa {info['empresa']} maior que 2<br><br>Valor no Makro: {converter_para_brl(valorMakro)}<br><br>Valor esperado: {converter_para_brl(valorX3po)}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return

        gerarRecibo = gerarReciboPagto(driver, info['empresa'])

        if gerarRecibo["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar recibo da folha de pagamento",
                'mensagem': f"Passo - Gerar recibo de pagamento.<br><br>Não foi possível gerar a folha de pagamento na empresa {info['empresa']}<br><br>{gerarRecibo['Mensagem']}"
            }
            enviarEmail(configEmail)
        
        gerarPeriodicos = gerar_periodicos(driver)
        if gerarPeriodicos["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar periodicos do e-Social",
                'mensagem': f"Passo - Gerar periódicos do e-social.<br><br>Não foi possível gerar os eventos periódicos do e-social na empresa {info['empresa']}<br><br>{gerarPeriodicos['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        entregarEventos = entregar_eventos(driver)
        if entregarEventos["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao entregar eventos do e-Social",
                'mensagem': f"Passo - Entregar eventos periódicos do e-social.<br><br>Não foi possível entregar os eventos do e-social na empresa {info['empresa']}<br><br>{entregarEventos['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return

        encerrarPessoal = encerrar_pessoal(driver)
        if encerrarPessoal["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao encerrar modulo pessoal",
                'mensagem': f"Passo - Encerrar módulo pessoal.<br><br>Não foi possível encerrar o modulo pessoal na empresa {info['empresa']}<br><br>{encerrarPessoal['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        entregarEventos = entregar_eventos(driver)
        if entregarEventos["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao entregar eventos do e-Social",
                'mensagem': f"Passo - Entregar evento 1299 do e-Social.<br><br>Não foi possível entregar os eventos do e-social na empresa {info['empresa']}<br><br>{entregarEventos['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        gerarDarf = baixarDarfRecibo(driver, info['empresa'])
        if gerarDarf["Execucao"] == False:
            configEmail = {
                'assunto': "Erro ao gerar e baixar darf ou recibo DCTFWeb",
                'mensagem': f"Passo - Gerar arquivos da DCTFWeb.<br><br>Não foi possível baixar os arquivos da DCTFWeb na empresa {info['empresa']}<br><br>{gerarDarf['Mensagem']}"
            }
            enviarEmail(configEmail)
            driver.quit()
            return
        
        if info['valorSimples'] > 0:
            emitirDas(driver, info['empresa'])

        atualizar_valor_fopag(info['cnpj'], info['periodoFinal'], revisarValor['Mensagem'])

        time.sleep(5)
        driver.quit()

        caminho_origem = r"Z:\\RPA\\Folha Pró-Labore\\Fopag Processada"
        caminho_destino = r"Z:\\RPA\Simples Nacional\\PGDAS-D processado"
        mover_arquivos(caminho_origem, caminho_destino)

    except Exception as e:
        configEmail = {
                'assunto': "Erro ao executar o processo",
                'mensagem': f"Não foi possível concluir o processo na empresa {info['empresa']}<br><br>{e}"
            }
        enviarEmail(configEmail)

def process_pdf(pdf_path):
    
    processo = leitorPgdasD(pdf_path)

    if processo[0] != "Processado com sucesso":
        time.sleep(10)
        processo = leitorPgdasD(pdf_path)

    # Especifique o caminho completo do arquivo PDF que você deseja mover
    pdf_path = pdf_path
    
    if processo[0] == "Processado com sucesso":
        
        logging.info(f"Documento processado com sucesso.")
        dest_directory = "Z:\RPA\Simples Nacional\PGDAS-D processado"
        info = processo[1]
        if info['issRetido'] == True:
            configEmail = {
                'assunto': "Apuração com ISS retido - Verificar.",
                'mensagem': f"Simples nacional declarado com ISS retido.<br><br>Foi encontrada informação de ISS retido na apuração do Simples Nacional da empresa {info['empresa']}<br><br>Verifique se deveria existir essa retenção, se estiver errado, refaça a declaração, reabra a folha de pagamento e reenvie para processamento no X3PO.<br><br>Caso esteja correto, não precisa tomar nenhuma ação."
            }
            enviarEmail(configEmail)

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
