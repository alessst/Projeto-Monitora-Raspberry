from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1258W9a_f08jn3wdDYs6jANfTHGQs0vCVARKTB5MlZc8'
SAMPLE_RANGE_NAME = 'aba'


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Adicionar uma nova linha com dados
        values = [["Item 1", "Item 2", "Item 3"]]
        body = {
            "range": SAMPLE_RANGE_NAME,
            "values": values,
        }
        result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()

        # Verificar se a operação foi bem sucedida
        print("Linha adicionada com sucesso!" if result.get("updates").get("updatedRows") > 0 else "Erro ao adicionar linha")
    
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
