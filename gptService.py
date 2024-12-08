import json
import os
from openai import OpenAI
from models.categories import Categories
from tests.transactionData import transaction_test_data
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Expenses(BaseModel):
    rent: list[float]
    groceries: list[float]
    travel: list[float]
    going_out: list[float]
    shopping: list[float]
    subscriptions: list[float]
    investments: list[float]
    savings: list[float]
    uncategorized: list[float]


class Income(BaseModel):
    salary: list[float]
    payments: list[float]


class Category(BaseModel):
    expenses: Expenses
    income: Income


class GptService:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    def categorize(self, transactions):
        categories = json.dumps(Categories().__dict__, indent=4)
        print(categories)
        # GPT call
        model = "gpt-4o-mini"
        result = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that categorizes financial transactions"
                        "Do not assign a transaction to multiple categories"
                        "Context: The transactions take place in germany. Use this information to accurately categorize the transactions."
                        "Remove any negative signs from the transaction amounts."
                    ),
                },
                {
                    "role": "assistant",
                    "content": (
                        "{'expenses': {'rent': [595.0], 'groceries': [3.25, 21.24, 16.53, 17.99, 101.77, 118.0], 'travel': [46.55], 'going_out': [22.6], 'shopping': [39.95, 31.95, 17.54, 29.99, 172.26, 39.88, 13.54, 28.88], 'subscriptions': [5.99, 1.0, 11.53], 'investments': [250.0, 500.0], 'uncategorized': [3.6, 4.5, 7.8, 1.99, 36.0, 3.9]}, 'income': {'salary': [3717.48], 'payments': [5.0, 7.5]}}"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Categorize the following transactions into the provided categories."
                        "Transactions to the Deutsche Bahn (DB) and to gas stations are to be categorized as travel."
                        f"Transactions with an even amount to {os.getenv("ACCOUNT_OWNER")} and {os.getenv("ACCOUNT_OWNER_FULL_NAME")} are to be categorized as investments"
                        f"Transactions to {os.getenv("HOUSEHOLD_MEMBER")} where the transaction details do not suggest otherwise are to be categorized as groceries"
                        "Transactions to grocery stores like Aldi, Rewe, Kaufland, Edeka and so on, as well as to bakeries are to be categorized as groceries."
                        "Transactions to stores that sell clothing, electronics, furniture, etc., and non-food in general are to be categorized as shopping."
                        f"Transactions: {transactions}"
                    ),
                },
            ],
            response_format=Category,
        )
        print(result)
        categorized_json = json.loads(str(result.choices[0].message.content))
        print(categorized_json)
        return categorized_json


# GptService().categorize(transaction_test_data.transaction_data_filtered_2024),
