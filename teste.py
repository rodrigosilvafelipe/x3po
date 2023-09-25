import os
import glob

# Definir o diretório onde os arquivos estão localizados
diretorio = r"Z:\\RPA\\Folha Pró-Labore\\Fopag Processada"

# Criar um padrão de busca para encontrar arquivos que começam com "CadEmpregadosIdadeTempoEmpresa"
padrao = os.path.join(diretorio, "CadEmpregadosIdadeTempoEmpresa*")

# Usar glob para encontrar todos os arquivos que correspondem ao padrão
arquivos_encontrados = glob.glob(padrao)

# Verificar se algum arquivo foi encontrado
if not arquivos_encontrados:
    print("Nenhum arquivo encontrado.")
else:
    # Pegar o primeiro arquivo encontrado
    arquivo_antigo = arquivos_encontrados[0]
    
    # Definir o novo nome do arquivo
    novo_nome = os.path.join(diretorio, "NovoNomeDoArquivo.xlsx")  # Substitua pela extensão correta
    
    # Renomear o arquivo
    os.rename(arquivo_antigo, novo_nome)
    print(f"Arquivo {arquivo_antigo} renomeado para {novo_nome}")
