import requests
import json
import time

# Solicitação de Iniciação
def get_device_code(client_id):
    url = "https://accounts.zoho.com/oauth/v3/device/code"
    payload = {
        "client_id": client_id,
        "scope": 'ZohoSheet.dataAPI.UPDATE,ZohoSheet.dataAPI.READ',
        "grant_type": "device_request",
        "access_type": "offline"
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Solicitação de Polling
def get_access_token(client_id, client_secret, device_code):
    url = f"https://accounts.zoho.com/oauth/v3/device/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "device_token",
        "code": device_code
    }
    
    # O polling deve ser feito em intervalos regulares até que o usuário complete a autenticação
    # ou até que o tempo máximo de espera seja atingido.
    max_attempts = 30  # Ajuste conforme necessário
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print("Attempt", attempt + 1, ":", response.text)
            attempt += 1
            time.sleep(5)  # Aguarde 5 segundos antes da próxima tentativa
    
    print("Failed to retrieve access token after", max_attempts, "attempts.")
    return None

def refresh(refresh_token, client_id, client_secret):
    base_url = "https://accounts.zoho.com/oauth/v2/token"    
 
    payload = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # Fazendo a requisição GET para obter os dados da planilha
    response = requests.post(base_url, payload)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Retornando os dados da planilha como JSON
        # print(response.json())
        return response.json()
    else:
        # Imprimindo a mensagem de erro e retornando None
        # print("Error:", response.status_code, response.text)
        return None

def get_sheet_data(access_token, sheet_id):
    # URL para a API do Zoho Sheet
    base_url = "https://sheet.zoho.com/api/v2/"
    
    # Construindo o URL para acessar os dados da planilha específica
    sheet_url = f"{base_url}{sheet_id}"
    
    # Headers para a requisição
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    payload = {
        "method": "worksheet.records.fetch",
        "worksheet_name": "Folha1",
    }
    
    # Fazendo a requisição GET para obter os dados da planilha
    response = requests.post(sheet_url, payload, headers=headers)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Retornando os dados da planilha como JSON
        # print(response.json())
        return response.json()
    else:
        # Imprimindo a mensagem de erro e retornando None
        # print("Error:", response.status_code, response.text)
        return None

def outrosVinculos(empresa):
    try:
        client_id = '1004.Q717391LMGC73P7I2C1LE1KL7DAZJW'
        client_secret = '3086d611c108b86692b5720f9ea8424b07b592714c'

        # inicializacao = get_device_code(client_id)
        # device_code = '1004.232d0fa6e95f6f9eb5aa10b7f707dcee.e4f5b98a35f38369a396254f2a0a0ffe'

        # access = get_access_token(client_id, client_secret, device_code)
        # access_token = '1004.64e8f033766f6b09ba584603b41cac73.e71c8db4b779a1261b08759dda295d19'
        refresh_token = '1004.58ae57af45e9fbbd1f05033be2f33945.b8d66321cdb263094e3a9788a80e8325'

        new_token = refresh(refresh_token, client_id, client_secret)

        sheet = get_sheet_data(new_token['access_token'], 'h47h2be1b4378cdd34edcaec397d218192be9')

        for record in sheet.get('records', []):
            if empresa.lower() in record.get('CLIENTES COM CONTRACHEQUE', '').lower():
                return {"Execucao": True, "Mensagem": False}
        return {"Execucao": True, "Mensagem": True}
    
    except Exception as e:
            return {"Execucao": False, "Mensagem": True, "Erro": e}
    
# Exemplo de uso
# Substitua YOUR_ACCESS_TOKEN e YOUR_SHEET_ID pelos valores reais
# access_token = "YOUR_ACCESS_TOKEN"
# sheet_id = "YOUR_SHEET_ID"

# sheet_data = get_sheet_data(access_token, sheet_id)

# if sheet_data:
#     print(json.dumps(sheet_data, indent=4))
# else:
#     print("Failed to retrieve data.")
