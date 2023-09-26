import os
import shutil

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
            return e
        
    return