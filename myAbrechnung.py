from dkb_robo import DKBRobo
import calendar
from datetime import datetime
import getpass
from gptService import GptService
from sheetsWriter import SheetsWriter


class Abrechnung:
    def start(self):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        month = int(input("Enter month as integer between 1 and 12: "))
        with DKBRobo(
            dkb_user=username,
            dkb_password=password,
            chip_tan=False,
            mfa_device=3,
            debug=False,
        ) as dkb:
            self.dkb = dkb
            print("Successfully logged in")
            self.date_range = self.getDateRange(month=month)
            transactions = self.getTransactionsInDateRange(self.date_range)
            self.transactions: list[dict[str, str]] = transactions
            print(
                "Date range: "
                + str(self.date_range.get("date_from"))
                + " - "
                + str(self.date_range.get("date_to"))
            )
            filteredTransactions = self.filterTransactionData()
            categories = self.categorizeTransactions(filteredTransactions)
            self.writeToCategoriesInSheets(categories)

    def getDateRange(self, month=None, year=None):
        startDate = self.getStartDate(month, year)
        endDate = self.getEndDate(startDate)
        return {
            "date_from": startDate.strftime("%d.%m.%Y"),
            "date_to": endDate.strftime("%d.%m.%Y"),
        }

    def getStartDate(self, month=None, year=None):
        today = datetime.today()
        if month is None:
            return today.replace(day=1).date()
        if year is None:
            year = today.year
        if not 1 <= month <= 12:
            raise ValueError("Month must be an integer between 1 and 12.")
        # Return the first day of the specified month
        return today.replace(year=year, month=month, day=1).date()

    def getEndDate(self, startDate):
        _, lastDayOfMonth = calendar.monthrange(startDate.year, startDate.month)
        return startDate.replace(day=lastDayOfMonth)

    def getTransactionsInDateRange(self, dateRange):
        giro_account = self.getGiroAccount()
        transactions_link = giro_account.get("transactions")
        transactions = self.dkb.get_transactions(
            transactions_link,
            "account",
            dateRange.get("date_from"),
            dateRange.get("date_to"),
        )
        return transactions

    def getGiroAccount(self):
        giro_account = self.dkb.account_dic.get(0)
        if giro_account == None:
            print("No giro account found")
            exit(1)
        return giro_account

    def sumTransactions(self):
        total = 0
        for transaction in self.transactions:
            # Get the 'amount' key and handle missing or invalid data
            amount = transaction.get("amount")
            if isinstance(amount, (int, float)):
                total += amount
            elif isinstance(amount, str):
                try:
                    total += float(amount)
                except ValueError:
                    continue
        return total

    def filterTransactionData(self):
        filtered_data = [
            {
                "amount": transaction.get("amount"),
                "customerreferenz": transaction.get("customerreferenz"),
                "peer": transaction.get("peer"),
                "postingtext": transaction.get("postingtext"),
                "reasonforpayment": transaction.get("reasonforpayment"),
            }
            for transaction in self.transactions
        ]
        return filtered_data

    def categorizeTransactions(self, transactions):
        categories = GptService().categorize(transactions)
        return categories

    def writeToCategoriesInSheets(self, categories):
        # extract categories from JSON
        # write them to the appropriate cell in google sheet
        writer = SheetsWriter()
        with writer:
            expenses = categories.get("expenses")
            groceries = expenses.get("groceries")
            writer.writeToCell("Lebensmittel!", groceries)
            travel = expenses.get("travel")
            writer.writeToCell("Reisen!", travel)
            going_out = expenses.get("going_out")
            writer.writeToCell("Ausgehen!", going_out)
            shopping = expenses.get("shopping")
            writer.writeToCell("Shopping!", shopping)
            uncategorized = expenses.get("uncategorized")
            writer.writeToCell("Uncategorized!", uncategorized)

if __name__ == "__main__":
    Abrechnung().start()
