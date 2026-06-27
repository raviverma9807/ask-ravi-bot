from openai import AzureOpenAI
from prompts.system_prompt import SYSTEM_PROMPT


class OpenAIService:
    def __init__(self, endpoint, api_key, deployment, embedding_deployment):
        self.deployment = deployment
        self.embedding_deployment = embedding_deployment

        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-01",
            azure_endpoint=endpoint
        )

        return response.data[0].embedding

    def generate_answer(self, question, context, history):
        system_prompt = SYSTEM_PROMPT.format(context=context)

        # Keep only the last few messages to maintain context
        conversation = history[-6:] if len(history) > 6 else history

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(conversation)

        # Ensure the current question is always the final message
        if not conversation or conversation[-1]["role"] != "user":
            messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

        response = self.client.chat.completions.create(
            model=self.deployment,
            temperature=0.2,
            max_tokens=900,
            messages=messages
        )

        return response.choices[0].message.content.strip()


    def generate_embedding(self, text):
        response = self.client.embeddings.create(
            model=self.embedding_deployment,
            input=text
        )

        return response.data[0].embedding