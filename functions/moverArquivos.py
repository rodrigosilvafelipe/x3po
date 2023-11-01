import shutil
import os
import datetime
import time

def mover_arquivos(caminho_origem, caminho_destino):

    # Listar todos os arquivos no diretório de origem
    arquivos = os.listdir(caminho_origem)
    
    # Iterar sobre cada arquivo
    for arquivo in arquivos:
        try:
            # Construir o caminho completo para o arquivo
            caminho_arquivo_origem = os.path.join(caminho_origem, arquivo)
            
            # Verificar se é um arquivo (e não um diretório)
            if os.path.isfile(caminho_arquivo_origem) and caminho_arquivo_origem.endswith(".pdf"):
                # Construir o caminho completo para o destino
                caminho_arquivo_destino = os.path.join(caminho_destino, arquivo)
                
                # Verificar se o arquivo já existe no destino
                if os.path.exists(caminho_arquivo_destino):
                    # Excluir o arquivo existente
                    os.remove(caminho_arquivo_destino)
                    # print(f"Arquivo {arquivo} existente foi removido do destino.")
                
                # Mover o arquivo
                shutil.move(caminho_arquivo_origem, caminho_arquivo_destino)
                # print(f"Arquivo {arquivo} movido com sucesso!")
            # else:
                # print(f"{arquivo} não é um arquivo e foi ignorado.")
        except Exception as e:

            # Obtem a data e hora atuais e formata conforme desejado
            data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Formata a mensagem de erro
            mensagem_erro = (
                "--------------------\n"
                + "Data e Hora: " + data_hora_atual + "\n"
                + "Erro: " + str(e) + "\n"
            )
            
            # Adiciona a mensagem de erro ao arquivo log.txt
            with open("Z:\\RPA\\Simples Nacional\\log-mover-arquivos.txt", "a") as log_file:
                log_file.write(mensagem_erro)

            # print(f"Erro: {str(e)}")
            pass
    
    return

# Usando a função
# caminho_origem = r"Z:\\RPA\\Folha Pró-Labore\\Fopag Processada"
# caminho_destino = r"Z:\\RPA\Simples Nacional\\PGDAS-D processado"
# mover_arquivos(caminho_origem, caminho_destino)
