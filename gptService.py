import json
import os
from openai import OpenAI
from models.categories import Categories
from tests.transactionData import transaction_test_data
from dotenv import load_dotenv

load_dotenv()


class GptService:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    def categorize(self, transactions):
        categories = json.dumps(Categories().__dict__, indent=4)
        print(categories)
        # GPT call
        model = "gpt-4o-mini"
        result = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that categorizes financial transactions into JSON data "
                        "based on user-provided categories. Ensure that each transaction is only assigned to one category."
                        "You output only JSON data."
                        "Your output does not contain any additional text, explanations, or formatting."
                        "Ensure the output is valid, well-formed JSON, without any escape characters, extra spaces, or newlines."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Categorize the following transactions into the provided categories."
                        "Use the transaction amounts and assign them to the appropriate category array."
                        "Context: The transactions take place in germany. Use this information to accurately categorize the transactions."
                        "Transactions to the Deutsche Bahn (DB) and to gas stations are to be categorized as travel."
                        f"Transactions to {os.getenv("ACCOUNT_OWNER")} are to be categorized as investments"  
                        f"Transactions to {os.getenv("HOUSEHOLD_MEMBER")} where the transaction details do not suggest otherwise are to be categorized as groceries"
                        "Transactions to grocery stores like Aldi, Rewe, Kaufland, Edeka and so on, as well as to bakeries are to be categorized as groceries."
                        "Transactions to stores that sell clothing, electronics, furniture, etc., and non-food in general are to be categorized as shopping."
                        "Return the result as JSON in the same structure as the input categories."
                        "Ensure only the numeric amounts are included in the arrays."
                        f"Categories: {categories}"
                        f"Transactions: {transactions}"
                    ),
                },
            ],
        )
        categorized_json = json.loads(str(result.choices[0].message.content))
        print(categorized_json)
        return categorized_json


# GptService().categorize(transaction_test_data.transaction_data_filtered_2024),
