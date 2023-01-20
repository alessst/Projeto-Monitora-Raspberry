import pandas as pd
import os
import time
import subprocess

with open('/proc/cpuinfo') as f:
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

mac_ethernet = subprocess.check_output("cat /sys/class/net/eth0/address", shell=True)
mac_ethernet = str(mac_ethernet)
mac_ethernet = mac_ethernet.replace("b'", "")
mac_ethernet = mac_ethernet.replace("'", "")
mac_ethernet = mac_ethernet.replace("\\n", "")
mac_ethernet = mac_ethernet.strip()


mac_wifi = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True)
mac_wifi = str(mac_wifi)
mac_wifi = mac_wifi.replace("b'", "")
mac_wifi = mac_wifi.replace("'", "")
mac_wifi = mac_wifi.replace("\\n", "")
mac_wifi = mac_wifi.strip()


dicionario = {"Modelo CPU":[model_name], "Hardware": [hardware] ,"Revisão": [revision] , "Serial": [serial], "Modelo Rasp" : [model],
              "MacAddress Ethernet": [mac_ethernet], "MacAddress Wifi": [mac_wifi] }


for chave in dicionario.keys():
  print(f'{chave} :{dicionario[chave]}')
  
  
df = pd.DataFrame(dicionario)

# caminho do arquivo
filepath = '/home/rasp/Projeto-Monitora-Raspberry-master/dados.csv'

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
