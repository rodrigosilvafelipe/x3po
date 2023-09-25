import openpyxl

def dadosRelacaoEmpregados(xlsx_path):
    try:
        # Abrir o arquivo Excel
        workbook = openpyxl.load_workbook(xlsx_path)

        # Selecionar a planilha ativa (ou você pode selecionar uma planilha específica pelo nome)
        sheet = workbook.active

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

        # Exibir o dicionário criado
        print(empregados_dict)

        return {'execução': True, 'mensagem': 'Processado com sucesso', 'dados': empregados_dict}
    
    except Exception as e:
        
        return {'execução': False, 'mensagem': e}
