import openpyxl
import re
import datetime

def dadosRelacaoEmpregados(xlsx_path, cnpj):
    
    try:
        # Abrir o arquivo Excel
        workbook = openpyxl.load_workbook(xlsx_path)

        # Selecionar a planilha ativa (ou você pode selecionar uma planilha específica pelo nome)
        sheet = workbook.active

        # Extrair o CNPJ da célula B7
        cnpj_celula = sheet['B7'].value
        
        # Usar expressão regular para extrair o CNPJ do texto
        cnpj_extraido = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj_celula)
        
        if cnpj_extraido:
            cnpj_extraido = cnpj_extraido.group()

        else:
            return {'execução': False, 'mensagem': 'CNPJ não encontrado no relatório'}
        
        # Comparar o CNPJ extraído com o CNPJ fornecido
        if cnpj_extraido != cnpj:
            return {'execução': False, 'mensagem': 'Relatório Relação de Empregados não pertence à empresa atual'}
        
        # Inicializar o dicionário para armazenar os dados extraídos
        empregados_dict = {}

        # Definir a linha inicial e as colunas para ler
        start_row = 12  # A linha onde o cabeçalho da tabela começa
        empregado_col = 'C'  # A coluna do empregado
        profissao_col = 'I'  # A coluna da profissão
        salario_col = 'L'  # A coluna do salário
        check_col = 'C'  # A coluna para verificar se a célula está vazia

        # Iterar sobre as linhas da tabela e extrair os dados
        row = start_row + 1  # Começar da linha abaixo do cabeçalho
        while sheet[f'{check_col}{row}'].value is not None:
            empregado = sheet[f'{empregado_col}{row}'].value
            profissao = sheet[f'{profissao_col}{row}'].value
            salario = sheet[f'{salario_col}{row}'].value

            # Adicionar os dados extraídos ao dicionário
            empregados_dict[empregado] = {'profissão': profissao, 'salário': salario}
            
            # Mover para a próxima linha
            row += 1

        return {'execução': True, 'mensagem': 'Processado com sucesso', 'dados': empregados_dict}
    
    except Exception as e:
        
        return {'execução': False, 'mensagem': e}
