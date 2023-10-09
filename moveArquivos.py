import shutil
import os
import time

# Caminhos das pastas
origem = r"Z:\RPA\Simples Nacional\Enviar para X3PO"
destino = r"Z:\RPA\Simples Nacional\PGDAS-D a processar"

while True:
    try:
        # Lista todos os arquivos na pasta de origem
        arquivos = os.listdir(origem)
        
        # Move cada arquivo para a pasta de destino
        for arquivo in arquivos:
            shutil.move(os.path.join(origem, arquivo), os.path.join(destino, arquivo))
        
        # Espera 10 segundos antes de mover os próximos arquivos
        time.sleep(10)
    
    except Exception as e:
        # print(f"Erro: {str(e)}")
        # Formata a mensagem de erro
        mensagem_erro = "--------------------\n" + "Erro: " + str(e) + "\n"
        
        # Adiciona a mensagem de erro ao arquivo log.txt
        with open("log.txt", "a") as log_file:
            log_file.write(mensagem_erro)
        # Espera 10 segundos antes de tentar novamente
        time.sleep(10)
