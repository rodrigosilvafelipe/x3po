import subprocess
import os
import threading

# Função para executar o primeiro script
def executar_script1():
    caminho_relativo_script = "observadorPgdasD.py"
    caminho_completo_script = os.path.abspath(caminho_relativo_script)
    comando = f"python {caminho_completo_script} --start"
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if resultado.returncode == 0:
        print("Script 1 executado com sucesso:")
        print(resultado.stdout)
    else:
        print("Erro ao executar o Script 1:")
        print(resultado.stderr)

# Função para executar o segundo script
def executar_script2():
    caminho_relativo_script2 = "observadorStartFopag.py"
    caminho_completo_script2 = os.path.abspath(caminho_relativo_script2)
    comando2 = f"python {caminho_completo_script2} --start"
    resultado2 = subprocess.run(comando2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if resultado2.returncode == 0:
        print("Script 2 executado com sucesso:")
        print(resultado2.stdout)
    else:
        print("Erro ao executar o Script 2:")
        print(resultado2.stderr)

# Crie duas threads para executar os scripts
thread1 = threading.Thread(target=executar_script1)
thread2 = threading.Thread(target=executar_script2)

# Inicie as threads
thread1.start()
thread2.start()

# Aguarde até que ambas as threads terminem
thread1.join()
thread2.join()

print("Ambas as threads terminaram de executar")
