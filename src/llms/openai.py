from .base import LLM
from openai import OpenAI

class GPT_3_5(LLM):
    def __init__(self, api_key):
        self.client = OpenAI(api_key = api_key)
        # self.messages = [
        #     {"role": "system",
        #      "content": "You are a intelligent assistant."}
        # ]

    def generate(self, prompt):
        # self.messages.append(
        #      {"role": "user",
        #       "content": prompt}
        # )
        response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=prompt)
        reply = response.choices[0].message.content
        # self.messages.append(
        #      {"role": "assistant"¯
        #       "content": reply}
        # )
        return reply
    
    def stream(self, prompt):
        for response in self.client.chat.completions.create(model="gpt-3.5-turbo", messages=prompt, stream=True):
            yield (response.choices[0].delta.content or "")