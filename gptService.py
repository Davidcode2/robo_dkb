from openai import OpenAI


class GptService:
    client = OpenAI()

    def categorize(self, transactions):
        categories = {
            "expenses": [
                {"rent": []},
                {"groceries": []},
                {"travel": []},
                {"going_out": []},
                {"shopping": []},
                {"subscriptions": []},
                {"investments": []},
                {"savings": []},
                {"uncategorized": []},
            ],
            "income": [{"salary": []}, {"payments": []}],
        }
        # GPT call
        return categories

    def testGpt(self):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Provide some ideas on the power of using an LLM in a program",
                },
            ],
        )
        print(completion.choices[0].message)

GptService().testGpt()
