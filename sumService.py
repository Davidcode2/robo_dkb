import os

class SumService:
    def sumTransactions(self, transactions):
        totalIncome = 0
        totalExpenses = 0
        totalInvest = 0
        for transaction in transactions:
            peer = str(transaction.get("peer")).lower()
            amount = transaction.get("amount")
            if isinstance(amount, (int, float, str)):
                floatAmount = float(amount)
                print(floatAmount);
                if self.checkIfInvestment(peer):
                    if floatAmount % 1 != 0 and floatAmount < 0:
                        continue
                    totalInvest += abs(floatAmount)
                    continue
                if floatAmount > 0:
                    totalIncome += abs(floatAmount)
                else:
                    totalExpenses += abs(floatAmount)
        return {
            "income": totalIncome,
            "expenses": totalExpenses,
            "investments": totalInvest,
        }

    def checkIfInvestment(self, peer):
        account_owner = str(os.getenv("ACCOUNT_OWNER")).lower()
        account_owner_full_name = str(os.getenv("ACCOUNT_OWNER_FULL_NAME")).lower()
        investmentBank = str(os.getenv("INVESTMENT_BANK")).lower()
        return (
            account_owner in peer
            or account_owner_full_name in peer
            or investmentBank in peer
        )
