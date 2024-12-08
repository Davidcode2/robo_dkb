import gptService
import unittest
from tests.transactionData import transaction_test_data


class TestGptService(unittest.TestCase):

    def test_categorize(self):
        _gptService = gptService.GptService()
        self.assertEqual(
            _gptService.categorize(
                transaction_test_data.transaction_data_filtered_2024
            ),
            {
                "expenses": [
                    {"rent": []},
                    {"groceries": [84.18]},
                    {"travel": []},
                    {"going_out": [1.49]},
                    {"shopping": [700.05]},
                    {"subscriptions": []},
                    {"investments": []},
                    {"savings": []},
                    {"uncategorized": []},
                ],
                "income": [{"salary": []}, {"payments": []}],
            },
        )


if __name__ == "__main__":
    unittest.main()
