"""Implement Yandex.Mail auth and scrapping methods by main class."""
# CHANGED: OAuth авторизация пользователя в почту
# CHANGED: Сборка писем с даты start_date по дату end_date
# CHANGED: Письма должны выбираться исходя из темы
# CHANGED: Разные темы в разные списки. Так же скачивание прикрепленных файлов
# CHANGED: Сохранение данных по страниам в Excel файл
# CHANGED: Имплементация класса для работы с Excel файлами
import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
import datetime
import csv
import pandas


class GMail():
    """Implementation of GMail API for user."""

    def __init__(
        self: 'GMail',
        token_filename: str = 'token.json',
        creds_filename: str = 'credentials.json'
    ):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None

        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(token_filename):
            creds = Credentials.from_authorized_user_file(
                token_filename, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_filename, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_filename, 'w') as token:
                token.write(creds.to_json())

        try:
            self._service = build('gmail', 'v1', credentials=creds)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def get_messages(
        self,
        from_data: tuple[int, int, int] = None,
        to_data: tuple[int, int, int] = None
    ):
        """Get list of messages from date to date.

        -----------------------------------------
        Returns <dict>
        """
        from_timestamp = int(datetime.datetime.strptime(
            f'{from_data[0]}.{from_data[1]}.{from_data[2]}',
            '%d.%m.%Y').timestamp()) * 1000

        to_timestamp = int(datetime.datetime.strptime(
            f'{to_data[0]}.{to_data[1]}.{to_data[2]}',
            '%d.%m.%Y').timestamp()) * 1000

        request = self._service.users().messages().list(
            userId='me', maxResults=500, q='На турбо-странице')

        response = request.execute()

        att_ids = dict()

        while True:

            if 'messages' not in response:
                continue

            for item in response['messages']:
                id = item['id']

                msg = self._service.users().messages().get(
                    userId='me', id=id).execute()

                if int(msg['internalDate']) < from_timestamp \
                        or int(msg['internalDate']) > to_timestamp:
                    continue

                if 'parts' in msg['payload'] and \
                        isinstance(msg['payload']['parts'], list):
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/csv':
                            for item in msg['payload']['headers']:
                                if item['name'] == 'Subject':
                                    fname = part['filename']
                                    att_id = part['body']['attachmentId']
                                    att_ids[fname] = f'{att_id}_{item["value"]}'

                for key in att_ids:
                    res = self._service.users().messages().attachments().get(
                        userId='me', messageId=id, id=att_ids[key]).execute()
                    with open(f'csv/{key}', 'wb') as file:
                        file.write(base64.urlsafe_b64decode(
                            res['data']))

            if 'nextPageToken' not in response:
                break

            request = self._service.users().messages().list_next(
                request, response)
            response = request.execute()

        self._files = att_ids

    def _parse_files(self: 'GMail', unique: str):
        vars = list()
        data = list()

        if len(self._files) < 1:
            return None

        for filename in self._files:
            rows = list()
            with open(f'csv/{filename}', 'r', encoding='utf-8') as file:
                rd = csv.reader(file, delimiter=';')
                for row in rd:
                    rows.append(row)
                rows.append(filename.split('_')[:-4])
            vars += rows[0]

            temp = dict()
            for key, value in zip(rows[0], rows[1]):
                temp[key] = value

            data.append(temp)

        vars = set(vars)
        for item in data:
            temp_vars = vars.copy()
            for key in item:
                if key in vars:
                    temp_vars.remove(key)

            for key in temp_vars:
                item[key] = ''

        with open(f'temp_{unique}.csv', 'w', encoding='utf-8') as file:
            wt = csv.writer(file)

            wt.writerow(sorted(list(vars)))
            for item in data:
                temp_data = list()
                for key in sorted(list(vars)):
                    temp_data.append(item[key])
                wt.writerow(temp_data)

        rf = pandas.read_csv(f'temp_{unique}.csv')
        rf.to_excel(f'excel/{unique}.xlsx', index=None, header=True)
        os.remove(f'temp_{unique}.csv')
        return f'excel/{unique}.xlsx'

    def get_file(
        self: 'GMail',
        from_date: tuple[int, int, int] = None,
        to_date: tuple[int, int, int] = None,
        message_id: str = None
    ) -> str:
        self.get_messages(from_date, to_date)
        return self._parse_files(message_id)
