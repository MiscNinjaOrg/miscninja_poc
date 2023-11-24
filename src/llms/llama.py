from .base import LLM
from llama_cpp import Llama

class LLAMA(LLM):
    def __init__(self, model_path, context_length=512, chat_format="llama-2"):
        self.n_ctx = context_length
        self.llm = Llama(model_path=model_path, chat_format=chat_format, n_ctx=self.n_ctx)
    
    def generate(self, prompt):
        response = self.llm.create_chat_completion(prompt, max_tokens=self.n_ctx, stop=["Q:", "\n"])
        return response
    
    def stream(self, prompt):
        for response in self.llm.create_chat_completion(prompt, max_tokens=self.n_ctx, stop=["Q:", "\n"], stream=True):
            if "content" in response['choices'][0]['delta']:
                yield response['choices'][0]['delta']['content']