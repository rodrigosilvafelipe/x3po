import subprocess
import os

# Caminho relativo para o arquivo "observadorPgdasD.py" a partir do diretório atual
caminho_relativo_script = "observadorPgdasD.py"

# Obtenha o caminho absoluto para o arquivo "observadorPgdasD.py" usando o caminho relativo
caminho_completo_script = os.path.abspath(caminho_relativo_script)

# Comando que você deseja executar
comando = f"python {caminho_completo_script} --start"

# Execute o comando no Windows
resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Verifique se a execução foi bem-sucedida
if resultado.returncode == 0:
    print("Comando executado com sucesso:")
    print(resultado.stdout)
else:
    print("Erro ao executar o comando:")
    print(resultado.stderr)
    