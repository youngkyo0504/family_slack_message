import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsManager:
    def __init__(self):
        required_env_vars = [
            "GOOGLE_SHEETS_TYPE",
            "GOOGLE_SHEETS_PROJECT_ID",
            "GOOGLE_SHEETS_PRIVATE_KEY_ID",
            "GOOGLE_SHEETS_PRIVATE_KEY",
            "GOOGLE_SHEETS_CLIENT_EMAIL",
            "GOOGLE_SHEETS_CLIENT_ID",
        ]

        # 필수 환경 변수 검증
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        # private key 특수 처리 (개행 문자 변환)
        private_key = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY")
        if private_key:
            private_key = private_key.replace("\\n", "\n")

        credentials_dict = {
            "type": os.getenv("GOOGLE_SHEETS_TYPE"),
            "project_id": os.getenv("GOOGLE_SHEETS_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_SHEETS_PRIVATE_KEY_ID"),
            "private_key": private_key,
            "client_email": os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_SHEETS_CLIENT_ID"),
            "auth_uri": os.getenv("GOOGLE_SHEETS_AUTH_URI"),
            "token_uri": os.getenv("GOOGLE_SHEETS_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv(
                "GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL"
            ),
            "client_x509_cert_url": os.getenv("GOOGLE_SHEETS_CLIENT_X509_CERT_URL"),
            "universe_domain": "googleapis.com",
        }

        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials_dict, scopes=self.SCOPES
        )
        self.service = build("sheets", "v4", credentials=self.credentials)

    def read_range(self, spreadsheet_id: str, range_name: str):
        """
        특정 범위의 데이터를 읽어옵니다
        :param spreadsheet_id: 스프레드시트 ID
        :param range_name: 범위 (예: 'Sheet1!A1:B10')
        :return: 데이터 리스트
        """
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            return result.get("values", [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def write_range(self, spreadsheet_id: str, range_name: str, values: list):
        """
        특정 범위에 데이터를 씁니다
        :param spreadsheet_id: 스프레드시트 ID
        :param range_name: 범위 (예: 'Sheet1!A1:B10')
        :param values: 쓸 데이터 리스트
        :return: 업데이트된 셀 개수
        """
        try:
            body = {"values": values}
            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            return result.get("updatedCells")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def append_rows(self, spreadsheet_id: str, range_name: str, values: list):
        """
        특정 범위 끝에 새로운 행을 추가합니다
        :param spreadsheet_id: 스프레드시트 ID
        :param range_name: 범위 (예: 'Sheet1!A:B')
        :param values: 추가할 데이터 리스트
        :return: 추가된 행 개수
        """
        try:
            body = {"values": values}
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            return result.get("updates").get("updatedRows")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
