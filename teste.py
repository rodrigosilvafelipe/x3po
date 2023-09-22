import subprocess

# Caminho para o executável gerado pelo pyinstaller
executable_path = 'enviarEmail.exe'

# Argumentos para passar para o executável
args = ['--para', 'rodrigo@escritax.com.br', '--assunto', 'Assunto do Email', '--mensagem', 'Conteúdo do Email']

try:
    # Execute o executável como um subprocesso
    subprocess.run([executable_path] + args, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o subprocesso: {e}")
