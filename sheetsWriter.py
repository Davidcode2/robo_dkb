from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SheetsWriter:

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    FINANCES_SPREADSHEET_ID = "1G_hlmv2G0YgezmmKwhiRtqoUvKiZ0AimzarYfmbY9Uc"
    SHEETNAME = "Ausgaben!A4:B"

    def writeToSheets(self, categories):
        # Write to Google Sheets
        self.authorize()
        sheet = 
        pass

    def main(self):
      """Shows basic usage of the Sheets API.
      Prints values from a sample spreadsheet.
      """

      try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.FINANCES_SPREADSHEET_ID, range=self.SHEETNAME)
            .execute()
        )
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

    def authorizeWithSheets():
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

    if __name__ == "__main__":
      main()

