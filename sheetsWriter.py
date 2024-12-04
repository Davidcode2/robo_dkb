import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()


class SheetsWriter:

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/spreadsheets"]
    FINANCES_SPREADSHEET_ID = os.getenv("FINANCES_SPREADSHEET_ID")
    SHEETNAME = "GPT_categorization!"
    SHEETNAME_TEST = "GPT_categorization!A1:B4"
    RANGE = "A:G"

    def writeToSheets(self):
        # Write to Google Sheets
        creds = self.authorizeWithSheets()
        sheet = self.getSheet(creds)
        result = self.readFromSheets(sheet)
        self.testWriteToSheets(sheet)
        #self.write(sheet, categories)
        self.showResult(result)
        pass

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

    def write(self, sheet, categories):
        body = {"values": categories}
        result = (
            sheet.values()
            .update(
                spreadsheetId=self.FINANCES_SPREADSHEET_ID,
                range=str(self.SHEETNAME + self.RANGE),
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        return result

    def readFromSheets(self, sheet):
        result = (
            sheet.values()
            .get(spreadsheetId=self.FINANCES_SPREADSHEET_ID, range=self.SHEETNAME_TEST)
            .execute()
        )
        return result

    def showResult(self, result):
        try:
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            print("Name, Major:")
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print(f"{row[0]}, {row[1]}")
        except HttpError as err:
            print(err)

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

    def getSheet(self, creds):
        service = build("sheets", "v4", credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet

SheetsWriter().writeToSheets()
