import os

def agrupar_arquivos_txt(diretorio, arquivo_saida):
    """
    Agrupa vários arquivos .txt em um único arquivo.

    Parâmetros:
    - diretorio: O diretório onde os arquivos .txt estão localizados.
    - arquivo_saida: O nome do arquivo de saída onde o conteúdo agrupado será salvo.
    """
    # Lista para armazenar os nomes dos arquivos .txt
    arquivos_txt = []

    # Iterar sobre os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        # Verificar se o arquivo é um .txt
        if arquivo.endswith(".txt"):
            print(arquivo)
            arquivos_txt.append(arquivo)

    # Abrir o arquivo de saída
    with open(arquivo_saida, 'w', encoding='ANSI') as saida:
        # Iterar sobre os arquivos .txt e escrever seu conteúdo no arquivo de saída
        for arquivo_txt in arquivos_txt:
            print(arquivo_txt)
            with open(os.path.join(diretorio, arquivo_txt), 'r', encoding='ANSI') as entrada:
                # Escrever o conteúdo no arquivo de saída
                saida.write(entrada.read())
                # Adicionar uma quebra de linha entre os conteúdos de diferentes arquivos
                # saida.write("\n")

# Exemplo de uso:
agrupar_arquivos_txt('Z:\RPA\Simples Nacional\BD_Simples_Nacional', 'Z:\RPA\Simples Nacional\BD_Simples_Nacional\saida.txt')
