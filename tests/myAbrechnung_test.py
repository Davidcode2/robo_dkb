import myAbrechnung
import unittest
from tests.transactionData import transaction_test_data


class TestAbrechnung(unittest.TestCase):

    def test_getDateRange_2023_01(self):
        abrechnung = myAbrechnung.Abrechnung()
        self.assertEqual(
            abrechnung.getDateRange(1, 2023),
            {"date_from": "01.01.2023", "date_to": "31.01.2023"},
        )

    def test_getDateRange_2024_12(self):
        abrechnung = myAbrechnung.Abrechnung()
        self.assertEqual(
            abrechnung.getDateRange(12, 2024),
            {"date_from": "01.12.2024", "date_to": "31.12.2024"},
        )

    def test_getDateRange_2023_13(self):
        abrechnung = myAbrechnung.Abrechnung()
        with self.assertRaises(ValueError) as context:
            abrechnung.getDateRange(13, 2023)
            # Optionally check the exception message
        self.assertEqual(
            str(context.exception), "Month must be an integer between 1 and 12."
        )

    def test_getDateRange_2023_0(self):
        abrechnung = myAbrechnung.Abrechnung()
        with self.assertRaises(ValueError) as context:
            abrechnung.getDateRange(0, 2023)
            # Optionally check the exception message
        self.assertEqual(
            str(context.exception), "Month must be an integer between 1 and 12."
        )

    def test_getDateRange_2023_n1(self):
        abrechnung = myAbrechnung.Abrechnung()
        with self.assertRaises(ValueError) as context:
            abrechnung.getDateRange(-1, 2023)
            # Optionally check the exception message
        self.assertEqual(
            str(context.exception), "Month must be an integer between 1 and 12."
        )

    def test_getTransactionsInDateRange_2023(self):
        abrechnung = myAbrechnung.Abrechnung()
        abrechnung.transactions = transaction_test_data.transaction_data_2023
        self.assertEqual(abrechnung.sumTransactions(), -122.52)

    def test_getTransactionsInDateRange_2024(self):
        abrechnung = myAbrechnung.Abrechnung()
        abrechnung.transactions = transaction_test_data.transaction_data_2024
        self.assertEqual(abrechnung.sumTransactions(), -785.72)

if __name__ == "__main__":
    unittest.main()
