from .base import LLM
import openai

class Chat(LLM):
    def __init__(self, api_key):
        openai.api_key = api_key
        self.messages = [
            {"role": "system",
             "content": "You are a intelligent assistant."}
        ]

    def generate(self, prompt):
        self.messages.append(
             {"role": "user",
              "content": prompt}
        )
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        reply = response.choices[0].message.content
        self.messages.append(
             {"role": "assistant",
              "content": reply}
        )
        return reply