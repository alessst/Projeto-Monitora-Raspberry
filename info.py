from __future__ import print_function
import pandas as pd
import os
import subprocess
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1258W9a_f08jn3wdDYs6jANfTHGQs0vCVARKTB5MlZc8'
SAMPLE_RANGE_NAME = 'aba'
# caminho do arquivo
filepath = 'dados.csv'


'''with open('/proc/cpuinfo') as f:
    data = f.read()

# transforma os dados em uma lista
lista = data.split()

# pega da lista o model name e forma a string
model_name = lista[6:11]
model_name = " ".join(model_name)

# pega da lista o serial e forma a string
serial = lista[208]

# pega da lista o hardware e forma a string
hardware = lista[202]

# pega da lista o revision e forma a string
revision = lista[205]

# pega da lista o model e forma a string
model = lista[211:219]
model = " ".join(model)

# pega o mac address da ethernet e forma uma string
mac_ethernet = subprocess.check_output("cat /sys/class/net/eth0/address", shell=True)
mac_ethernet = str(mac_ethernet)
mac_ethernet = mac_ethernet.replace("b'", "")
mac_ethernet = mac_ethernet.replace("'", "")
mac_ethernet = mac_ethernet.replace("\\n", "")
mac_ethernet = mac_ethernet.strip()

# pega o mac address do wifi e forma uma string
mac_wifi = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True)
mac_wifi = str(mac_wifi)
mac_wifi = mac_wifi.replace("b'", "")
mac_wifi = mac_wifi.replace("'", "")
mac_wifi = mac_wifi.replace("\\n", "")
mac_wifi = mac_wifi.strip()'''

model_name = 1
hardware = 2
revision = 3
serial = 4 
model = 5
mac_ethernet = 6
mac_wifi = 7

dicionario = {"Modelo CPU":[model_name], "Hardware": [hardware] ,"Revisão": [revision] , "Serial": [serial], 
"Modelo Rasp" : [model], "MacAddress Ethernet": [mac_ethernet], "MacAddress Wifi": [mac_wifi] }

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

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        raise ValueError("Credenciais inválidas ou inexistentes.")

    try:
        
        service = build('sheets', 'v4', credentials=creds)

        # Adicionar uma nova linha com dados
        values = [[model_name, hardware, revision, serial, model, mac_ethernet, mac_wifi]]
        body = {
            "range": SAMPLE_RANGE_NAME,
            "values": values,
        }
        result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()

        # Verificar se a operação foi bem sucedida
        print("Linha adicionada com sucesso!" if result.get("updates").get("updatedRows") > 0 else "Erro ao adicionar linha")
    
    except HttpError as err:
        print(err)

arquivo_csv()
main()
