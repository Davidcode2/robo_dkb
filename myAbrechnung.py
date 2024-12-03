from dkb_robo import DKBRobo
import calendar
from datetime import datetime
from pprint import pprint
import getpass
from sheetsWriter import SheetsWriter

class Abrechnung: 
    def start(self):
        username = input("Enter username: ") 
        password = getpass.getpass("Enter password: ") 
        month = int(input("Enter month as integer between 1 and 12: "))
        with DKBRobo(dkb_user=username, dkb_password=password, chip_tan=False, mfa_device=3, debug=False) as dkb:
            self.dkb = dkb
            print("Successfully logged in")
            transactions = self.getTransactionsInDateRange(self.getDateRange(month=month))
            self.transactions: list[dict[str, str]]  = transactions
            print("Date range: " + str(self.getDateRange().get('date_from')) + " - " + str(self.getDateRange().get('date_to')))
            print("Transactions in the specified date range: ")
            filteredTransactions = self.filterTransactionData()
            pprint(filteredTransactions)
            categories = self.categorizeTransactions(filteredTransactions)
            SheetsWriter.writeToSheets(categories)

    def getDateRange(self, month=None, year=None):
        startDate = self.getStartDate(month, year)
        endDate = self.getEndDate(startDate)
        return { 'date_from': startDate.strftime('%d.%m.%Y'), 'date_to': endDate.strftime('%d.%m.%Y') }

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
        transactions_link = giro_account.get('transactions');
        transactions = self.dkb.get_transactions(transactions_link, "account", dateRange.get('date_from'), dateRange.get('date_to'))
        return transactions

    def getGiroAccount(self):
        giro_account = self.dkb.account_dic.get(0);
        pprint(giro_account)
        if (giro_account == None):
            print("No giro account found")
            exit(1)
        return giro_account

    def sumTransactions(self):
        total = 0
        for transaction in self.transactions:
            # Get the 'amount' key and handle missing or invalid data
            amount = transaction.get('amount')
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
                'amount': transaction.get('amount'),
                'bdate': transaction.get('bdate'),
                'customerreferenz': transaction.get('customerreferenz'),
                'peer': transaction.get('peer'),
                'postingtext': transaction.get('postingtext'),
                'reasonforpayment': transaction.get('reasonforpayment')
            }
            for transaction in self.transactions]
        return filtered_data

    def categorizeTransactions(self, transactions):
        categories = { 'income': 
                      [{'rent': []}, {'groceries': []}, {'travel': []}, {'going_out': []}, {'shopping': []}, {'subscriptions': []}, {'investments': []}, {'savings': []}, {'uncategorized': []}],
                      'expenses': 
                      [{'salary': []}, {'payments': []}] 
                     }
        # GPT call
        return categories;

if __name__ == "__main__":
    Abrechnung().start()
