import os
import shutil
import datetime
import time

def limparPasta(caminho_da_pasta):
    # Lista todos os arquivos e subpastas no caminho especificado
    for nome in os.listdir(caminho_da_pasta):
        # Construa o caminho completo para o arquivo ou subpasta
        caminho_completo = os.path.join(caminho_da_pasta, nome)
        
        try:
            # Se for uma subpasta, use shutil.rmtree para excluí-la
            if os.path.isdir(caminho_completo):
                shutil.rmtree(caminho_completo)
            # Se for um arquivo, use os.remove para excluí-lo
            else:
                os.remove(caminho_completo)

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
            
            pass
        
    return