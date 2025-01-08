from transformers import pipeline
from .base_llm import BaseLLM

class HuggingFaceLLM(BaseLLM):
    def __init__(self, model_id: str = "meta-llama/Llama-2-7b-chat-hf"):
        self.generator = pipeline(
            "text-generation",
            model=model_id,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.generator(prompt, max_length=512)
        return response[0]['generated_text']