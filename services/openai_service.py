from openai import AzureOpenAI
from prompts.system_prompt import SYSTEM_PROMPT


class OpenAIService:
    def __init__(self, endpoint, api_key, deployment):
        self.deployment = deployment
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-01",
            azure_endpoint=endpoint
        )

    def generate_answer(self, question, context, history):
        system_prompt = SYSTEM_PROMPT.format(context=context)

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(history)

        response = self.client.chat.completions.create(
            model=self.deployment,
            temperature=0.2,
            messages=messages
        )

        return response.choices[0].message.content.strip()