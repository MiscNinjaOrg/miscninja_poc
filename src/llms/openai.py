from .base import LLM
import openai

class Chat(LLM):
    def __init__(self, api_key):
        openai.my_api_key = api_key
        self.messages = [
            {"role": "system",
             "content": "You are a intelligent assistant."}
        ]

    def generate(self, prompt):
        self.messages.append(
             {"role": "user",
              "content": prompt}
        )
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = response.choices[0].message.content
        self.messages.append(
             {"role": "asssistant",
              "content": reply}
        )
        return reply