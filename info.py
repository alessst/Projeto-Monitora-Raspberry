import pandas as pd
import os

# Criando um dicionario
dicionario = {'coluna1': [1], 'coluna2': [2]}

# caminho do arquivo
filepath = 'dicionario.csv'

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
