import datetime

# Função para extrair e converter a data do campo 6
def extrair_e_converter_data(linha):
    campos = linha.strip().split('|')
    if len(campos) > 5:
        data_str = campos[5]  # Assumindo que o campo 6 contém a data no formato "DD/MM/AAAA"
        try:
            data_obj = datetime.datetime.strptime(data_str, "%d/%m/%Y")
            return data_obj
        except ValueError:
            return None
    else:
        return None

# Ler o arquivo de texto e verificar os campos 6, 9 e 12
with open("Z:\\RPA\\Simples Nacional\\BD_Simples_Nacional\\41064121000184.txt", 'r') as arquivo:
    linhas = arquivo.readlines()

# Obter a data atual
data_atual = datetime.datetime.now()

# Inicializar a soma
soma_campo_12 = 0

# Inicializar o valor do campo 9 de 12 meses atrás
valor_campo_9_12_meses_atras = 0

# Calcular a data há 12 meses a partir da data atual
data_12_meses_atras = data_atual - datetime.timedelta(days=365)

# Inicializar lista
apuracoes = {}

# Percorrer as linhas para calcular a soma
for linha in linhas:
    data = extrair_e_converter_data(linha)
    campos = linha.strip().split('|')
    valor_campo_9 = campos[8].replace(".", "")
    valor_campo_9 = valor_campo_9.replace(",", ".")
    valor_campo_12 = campos[11].replace(".", "")
    valor_campo_12 = valor_campo_12.replace(",", ".")
    valor_campo_9 = float(valor_campo_9)  # Assumindo que o campo 9 contém valores numéricos
    valor_campo_12 = float(valor_campo_12)  # Assumindo que o campo 9 contém valores numéricos
    competencia = datetime.datetime.strptime(campos[5], "%d/%m/%Y")

    info = {
        'receitaMes': valor_campo_9,
        'receitaAno': valor_campo_12,
        'receita13Meses': valor_campo_9 + valor_campo_12
    }
    apuracoes[competencia] = info

    # Calcular a data há 12 meses a partir da data atual
    data_12_meses_atras = competencia - datetime.timedelta(days=365)
    print(f"competencia: {competencia}")
    print(f"ano passsado: {data_12_meses_atras}")

    valor_encontrado = None

    # Iterar pelas chaves (datas) do objeto
    for data, valores in apuracoes.items():
        if data == data_12_meses_atras:
            valor_encontrado = valores
            break  # Se encontrou a data, interrompe o loop

    revisaRbt12 = 0
    print("Inicio revisao")
    # Iterar pelas chaves (datas) do objeto
    for data, valores in apuracoes.items():
        if data >= data_12_meses_atras:
            revisaRbt12 += valores['receitaMes']

    rbt12Base = round(revisaRbt12 - apuracoes[competencia]['receitaMes'], 2)
    if apuracoes[competencia]['receitaAno'] != rbt12Base:
        print("Erro na receita bruta calculada!")

    # Verifica se a data foi encontrada e, se sim, exibe os valores associados
    if valor_encontrado is not None:
        novaRbt12 = revisaRbt12 - valor_encontrado['receitaMes']
        apuracoes[competencia]['novaRBT12'] = round(novaRbt12, 2)
    else:
        apuracoes[competencia]['novaRBT12'] = round(revisaRbt12, 2)

    print(apuracoes[competencia]['novaRBT12'])

# Exibir a soma
# print("Resultado:", soma_campo_12)
# print(apuracoes)
