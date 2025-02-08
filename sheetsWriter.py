import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class SheetsWriter:

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    FINANCES_SPREADSHEET_ID = os.getenv("FINANCES_SPREADSHEET_ID")
    SHEETNAME_TEST = "GPT_categorization!A1:B4"

    def __init__(self, start_date):
        self.sheet = None
        self.sheet = self.getSheet(self.authorizeWithSheets())
        self.start_date = start_date

    def writeTotal(self, sheet_name, expenses, income, invest, start_date=None):
        print(f"Writing expenses ({round(expenses, 2)}) and income ({round(income, 2)}) to sheet {sheet_name}")
        start_row = self.get_last_row(sheet_name)
        self.writeMonth(sheet_name, start_row, start_date)
        self.writeValues(start_row, sheet_name, [expenses], "B")
        self.writeValues(start_row, sheet_name, [income], "C")
        self.writeValues(start_row, sheet_name, [invest], "D")

    def writeMonth(self, sheet_name, start_row, start_date=None):
        column = "A"
        if (start_date is None):
            date_header = self.createDateHeader(self.start_date)
        else:
            date_header = self.createDateHeader(start_date)
        headers = [[date_header]]
        cell_range = f"{column}{str(start_row)}"
        self.execute_update_sheet(str(sheet_name + cell_range), headers)

    def write(self, sheet_name, values):
        print(f"Writing {values} to sheet {sheet_name}")
        start_row = self.get_last_row(sheet_name)
        self.writeHeaders(sheet_name, start_row)
        self.writeValues(start_row, sheet_name, values)

    def writeValues(self, start_row, sheet_name, values, column = "C"):
        row_values = [values]
        cell_range = column + str(start_row) + ":" + str(start_row)
        self.execute_update_sheet(str(sheet_name + cell_range), row_values)

    def writeHeaders(self, sheet_name, start_row):
        column = "A"
        end_column = "B"
        date_header = self.createDateHeader(self.start_date)
        sum_formula = self.createSumFormula(start_row)
        headers = [[date_header, sum_formula]]
        cell_range = f"{column}{str(start_row)}:{end_column}{str(start_row)}"
        self.execute_update_sheet(str(sheet_name + cell_range), headers)

    def execute_update_sheet(self, sheet_range, values):
        self.sheet.values().update(
            spreadsheetId=self.FINANCES_SPREADSHEET_ID,
            range=str(sheet_range),
            valueInputOption="USER_ENTERED",
            body={"values": values},
        ).execute()

    def createDateHeader(self, start_date):
        yearAndMonth = start_date.strftime("%Y %B")
        return yearAndMonth

    def createSumFormula(self, start_row):
        start_column = "C"
        sumFormula = f"=SUM({start_column}{start_row}:{start_row})"
        return sumFormula

    def arrayToColumn(self, values):
        column_values = [[value] for value in values]
        return column_values

    def column_number_to_letter(self, column_number):
        """Convert a column number to a column letter (e.g., 1 -> A, 27 -> AA)."""
        column_letter = ""
        while column_number > 0:
            column_number -= 1
            column_letter = chr(column_number % 26 + 65) + column_letter
            column_number //= 26
        return column_letter

    def get_last_row(self, sheet_name):
        result = (
            self.sheet.values()
            .get(
                spreadsheetId=self.FINANCES_SPREADSHEET_ID,
                range=str(sheet_name + "A:Z"),
            )
            .execute()
        )
        values = result.get("values", [])
        row = len(values)
        first_empty_row = row + 1
        return first_empty_row

    def get_last_column(self, sheet_name):
        result = (
            self.sheet.values()
            .get(
                spreadsheetId=self.FINANCES_SPREADSHEET_ID,
                range=str(sheet_name + "A:Z"),
            )
            .execute()
        )
        values = result.get("values", [])

        # Determine the last column
        last_column = 0
        for row in values:
            if len(row) > last_column:
                last_column = len(row)
        first_empty_column = last_column + 1
        return first_empty_column

    def testWriteToSheets(self, sheet):
        mylist = [
            ["Name", "Major"],
            ["Patrick", "Computer Science"],
            ["John", "Biology"],
            ["Mary", "Math"],
        ]
        sheet.values().update(
            spreadsheetId=self.FINANCES_SPREADSHEET_ID,
            range=self.SHEETNAME_TEST,
            valueInputOption="USER_ENTERED",
            body={"values": mylist},
        ).execute()

    def authorizeWithSheets(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    @contextmanager
    def sheets_service(self, creds):
        service = build("sheets", "v4", credentials=creds)
        try:
            yield service.spreadsheets()
        finally:
            if hasattr(service._http, "close"):
                service._http.close()

    def getSheet(self, creds):
        with self.sheets_service(creds) as service:
            return service

    def __enter__(self):
        # Return self to allow usage in a context manager
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean up resources (if any)
        if hasattr(self.sheet, "close"):
            self.sheet.close()
        print("SheetsWriter resources have been cleaned up.")
