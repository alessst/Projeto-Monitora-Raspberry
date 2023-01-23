from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import pandas as pd
import subprocess
import socket
from datetime import datetime

# se modificar esses ESCOPOS, exclua o token do arquivo 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ID da Planilha e o nome da pagina.
SAMPLE_SPREADSHEET_ID = '1258W9a_f08jn3wdDYs6jANfTHGQs0vCVARKTB5MlZc8'
SAMPLE_RANGE_NAME = 'aba'

# caminho do arquivo
filepath = '/home/rasp/Projeto-Monitora-Raspberry-master/dados.csv'

ethernet = "eth0"
wifi = "wlan0"

# pega a hora que foi gerado o arquivo
def get_time():
    # pega a data e hora atuais
    current_time = datetime.now()
    # formata a data e hora em uma string
    time_string = current_time.strftime("%H:%M:%S %d/%m/%Y")
    return time_string


# envia os dados para um Arquivo CSV
def arquivo_csv():
    for chave in dicionario.keys():
        print(f'{chave} :{dicionario[chave]}')
            
        df = pd.DataFrame(dicionario)
        # verifica se o arquivo existe
        if os.path.exists(filepath):
            # Carrega o arquivo CSV em um DataFrame
            df = pd.read_csv(filepath)
            # cria um novo dataframe
            new_df = pd.DataFrame.from_dict(dicionario)
            # concatena os dataframes
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            # Cria DataFrame a partir do dicionario
            df = pd.DataFrame.from_dict(dicionario)
        # salvando o dataframe em csv
    df.to_csv(filepath, index=False)

# pega valor de ip da rede 
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # tenta se conectar a um endereço de broadcast para pegar o endereço IP
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# envia os dados para uma planilha via api do google
def planilha():
    creds = None
    
    if os.path.exists('/home/rasp/Projeto-Monitora-Raspberry-master/token.json'):
        creds = Credentials.from_authorized_user_file('/home/rasp/Projeto-Monitora-Raspberry-master/token.json', SCOPES)
    # Se não houver credenciais (válidas) disponíveis, deixe o usuário fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/rasp/Projeto-Monitora-Raspberry-master/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salve as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        
        service = build('sheets', 'v4', credentials=creds)

        # Adicionar uma nova linha com dados
        values = [[model_name, hardware, revision, serial, model, mac_ethernet, mac_wifi, ip_rede, hora]]
        body = {
            "range": SAMPLE_RANGE_NAME,
            "values": values,
        }
        result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()

        # Verificar se a operação foi bem sucedida
        print("Linha adicionada com sucesso!" if result.get("updates").get("updatedRows") > 0 else "Erro ao adicionar linha")
    
    except HttpError as err:
        print(err)



# Pega uma lista de informações da Raspberry
def info_rasp():
    with open('/proc/cpuinfo') as f:
        data = f.read()
    # transforma os dados em uma lista
    infor_rasp = data.split()
    return infor_rasp
lista = info_rasp()


def format_list(form_lista, numero1, numero2):
    if numero2 == 0:
        nome = form_lista[numero1]
    else:
        nome = form_lista[numero1:numero2]
        nome = " ".join(nome)
    return nome

def mac_address_valor(rede):
    # pega o mac address da ethernet e forma uma string
    mac_address = subprocess.check_output(f"cat /sys/class/net/{rede}/address", shell=True)
    mac_address = str(mac_address)
    mac_address = mac_address.replace("b'", "")
    mac_address = mac_address.replace("'", "")
    mac_address = mac_address.replace("\\n", "")
    mac_address = mac_address.strip()
    return mac_address

# pega da lista o model name e forma a string
model_name = format_list(lista, 6, 11)
# pega da lista o model e forma a string
model = format_list(lista, 211, 219)

# pega da lista o serial e forma a string
serial = format_list(lista, 208, 0)

# pega da lista o hardware e forma a string
hardware = format_list(lista, 202, 0)

# pega da lista o revision e forma a string
revision = format_list(lista, 205, 0)

# pega o mac address da ethernet e forma uma string
mac_ethernet = mac_address_valor(ethernet)

# pega o mac address do wifi e forma uma string
mac_wifi = mac_address_valor(wifi)

# coloca em uma variavel
ip_rede = get_ip()

# pega a hora da raspberry
hora = get_time()

dicionario = {"Modelo CPU":[model_name], "Hardware": [hardware] ,"Revisão": [revision] , "Serial": [serial], 
"Modelo Rasp" : [model], "MacAddress Ethernet": [mac_ethernet], "MacAddress Wifi": [mac_wifi], "IP": [ip_rede], "Horas": [hora] }

arquivo_csv()
planilha()
