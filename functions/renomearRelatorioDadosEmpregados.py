import os
import glob

def renomearRelatorio(pasta, novoNome):

    # Criar um padrão de busca para encontrar arquivos que começam com "CadEmpregadosIdadeTempoEmpresa"
    padrao = os.path.join(pasta, "CadEmpregadosIdadeTempoEmpresa*")

    # Usar glob para encontrar todos os arquivos que correspondem ao padrão
    arquivos_encontrados = glob.glob(padrao)

    # Verificar se algum arquivo foi encontrado
    if not arquivos_encontrados:
        return {"Execução": False, "Mensagem": "Não encontrei o relatório de Relação de Empregados no caminho esperado."}
        # print("Nenhum arquivo encontrado.")
    else:
        # Pegar o primeiro arquivo encontrado
        arquivo_antigo = arquivos_encontrados[0]
        
        # Definir o novo nome do arquivo
        novo_nome = os.path.join(pasta, f"{novoNome}.xlsx")  # Substitua pela extensão correta
        
        # Renomear o arquivo
        os.rename(arquivo_antigo, novo_nome)
        # print(f"Arquivo {arquivo_antigo} renomeado para {novo_nome}")
        return {"Execução": True, "Mensagem": "Processo concluído"}
