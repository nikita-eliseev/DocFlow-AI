from app.ai.openai_client import client


class AIService:
    def summarize_text(self, text: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You summarize documents clearly and shortly."
                    )
                },
                {
                    "role": "user",
                    "content": text[:12000]
                }
            ]
        )

        return response.choices[0].message.content
    