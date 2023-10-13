import shutil
import os
import datetime
import time

# Caminhos das pastas
origem = r"Z:\RPA\Simples Nacional\Enviar para X3PO"
destino = r"Z:\RPA\Simples Nacional\PGDAS-D a processar"

while True:
    try:
        # Lista todos os arquivos na pasta de origem
        arquivos = os.listdir(origem)
        
        # Verifica se ainda há arquivos para mover
        if arquivos:
            # Seleciona um arquivo para mover
            arquivo = arquivos[0]
            caminho_origem = os.path.join(origem, arquivo)
            caminho_destino = os.path.join(destino, arquivo)

             # Verifica se o arquivo já existe no destino
            if os.path.exists(caminho_destino):
                # Se existir, exclui o arquivo da pasta de origem
                os.remove(caminho_origem)
            else:
                # Se não existir, move o arquivo para a pasta de destino
                shutil.move(caminho_origem, caminho_destino)
            
            # Espera 5 segundos antes de mover o próximo arquivo
            time.sleep(5)
            
        else:
            # Se não há arquivos para mover, espera 60 segundos antes de verificar novamente
            time.sleep(60)
    
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
        
        # Espera 10 segundos antes de tentar novamente
        time.sleep(10)

        pass
