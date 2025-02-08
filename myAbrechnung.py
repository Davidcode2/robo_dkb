from dkb_robo import DKBRobo
import sys
import getpass
from calendarService import CalendarService
from gptService import GptService
from sheetsWriter import SheetsWriter
from sumService import SumService

class Abrechnung:
    sumService = SumService()

    def getYearArg(self):
        if (len(sys.argv) < 2):
            print("No arguments provided")
            exit(1)
        arg1 = sys.argv[1]
        if (int(arg1) > 2022 and int(arg1) < 2030):
            return int(arg1);
        else:
            print("Invalid argument for year.")
            exit(1)

    def getBalancesForYear(self):
        self.year = self.getYearArg()
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        with DKBRobo(
            dkb_user=username,
            dkb_password=password,
            chip_tan=False,
            mfa_device=3,
            debug=False,
        ) as dkb:
            self.dkb = dkb
            print("Successfully logged in\n")
            print("Calculating balance for year:", self.year)
            self.calendarService = CalendarService(year=self.year)
            for month in range(1,13):
                filteredTransactions = self.getTransactionsFor(month, self.year)
                sums = self.sumService.sumTransactions(filteredTransactions)
                self.writeTotalIncomeAndExpenses(sums, month)

    def categorize(self):
        month = int(input("Enter month as integer between 1 and 12: "))
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        with DKBRobo(
            dkb_user=username,
            dkb_password=password,
            chip_tan=False,
            mfa_device=3,
            debug=False,
        ) as dkb:
            self.dkb = dkb
            print("Successfully logged in")
            self.calendarService = CalendarService(month=month)
            filteredTransactions = self.getTransactionsFor(month)
            categories = self.categorizeTransactions(filteredTransactions)
            sums = self.sumService.sumTransactions(self.transactions)
            self.writeTotalIncomeAndExpenses(sums)
            self.writeToCategoriesInSheets(categories)

    def getTransactionsFor(self, month, year=None):
        date_range = self.calendarService.getDateRange(month=month, year=year)
        transactions = self.getTransactionsInDateRange(date_range)
        self.transactions: list[dict[str, str]] = transactions
        filteredTransactions = self.filterTransactionData()
        return filteredTransactions;

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

    def writeTotalIncomeAndExpenses(self, sums, month=None):
        income = sums.get("income")
        expenses = sums.get("expenses")
        investments = sums.get("investments")
        if month is None:
            start_date = self.calendarService.startDate
        else:
            start_date = self.calendarService.getStartDate(month, self.year)
        writer = SheetsWriter(start_date=start_date)
        print("\n")
        with writer:
            writer.writeTotal("Balance!", income, expenses, investments, start_date=start_date)

    def writeToCategoriesInSheets(self, categories):
        # extract categories from JSON
        # write them to the appropriate cell in google sheet
        writer = SheetsWriter(start_date=self.calendarService.startDate)
        print("\n")
        with writer:
            expenses = categories.get("expenses")
            groceries = expenses.get("groceries")
            writer.write("Lebensmittel!", groceries)
            travel = expenses.get("travel")
            writer.write("Reisen!", travel)
            going_out = expenses.get("going_out")
            writer.write("Ausgehen!", going_out)
            shopping = expenses.get("shopping")
            writer.write("Shopping!", shopping)
            uncategorized = expenses.get("uncategorized")
            writer.write("Uncategorized!", uncategorized)


if __name__ == "__main__":
    Abrechnung().getBalancesForYear()
