import datetime
import locale

def validadorReceitaBruta(caminho, compAtual, rbt12):

    # Função para extrair e converter a data do campo 6
    def extrair_e_converter_data(linha):
        campos = linha.strip().split('|')
        if len(campos) > 5:
            data_str = campos[5]  # Assumindo que o campo 6 contém a data no formato "DD/MM/AAAA"
            try:
                data_obj = datetime.datetime.strptime(data_str, "%d/%m/%Y")
                return data_obj
            except ValueError:
                return datetime.datetime(2000, 12, 31)
        else:
            return datetime.datetime(2000, 12, 31)

    # Ler o arquivo de texto e verificar os campos 6, 9 e 12
    with open(caminho, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Calcular a data há 12 meses a partir da data atual
    competencia = datetime.datetime.strptime(compAtual, "%d/%m/%Y")
    data_12_meses_atras = competencia - datetime.timedelta(days=365)

    # Inicializar lista
    apuracoes = {}

    # Percorrer as linhas para calcular a soma
    for linha in linhas:
        data = competencia
        campos = linha.strip().split('|')
        valor_campo_9 = campos[8].replace(".", "")
        valor_campo_9 = valor_campo_9.replace(",", ".")
        valor_campo_17 = campos[16].replace(".", "")
        valor_campo_17 = valor_campo_17.replace(",", ".")
        valor_campo_9 = float(valor_campo_9)  # Assumindo que o campo 9 contém valores numéricos
        valor_campo_17 = float(valor_campo_17)  # Assumindo que o campo 9 contém valores numéricos
        compApuracao = extrair_e_converter_data(linha)
        info = {
            'receitaMes': valor_campo_9,
            'cppMes': valor_campo_17,
        }
        apuracoes[compApuracao] = info

    valor_encontrado = None

    # Iterar pelas chaves (datas) do objeto
    for data, valores in apuracoes.items():
        if data == data_12_meses_atras:
            valor_encontrado = valores['receitaMes']
            break  # Se encontrou a data, interrompe o loop

    # print(valor_encontrado)
    rbt12Calculado = float(rbt12) - valor_encontrado

    revisaRbt12 = 0

    # Iterar pelas chaves (datas) do objeto
    for data, valores in apuracoes.items():
        if data >= data_12_meses_atras and data < competencia:
            revisaRbt12 += valores['receitaMes']

    rbt12Base = round(revisaRbt12, 2)

    return [rbt12Base, rbt12Calculado]
