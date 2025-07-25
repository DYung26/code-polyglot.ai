from typing import List
from src.ai.prompts import build_instruction_prompt, build_translation_prompt
from .client import get_client


class AIEngine:
    def __init__(self, model="gpt-4o"):
        self.client = get_client()
        self.model = model

    def translate_module(self, text: str, current_lang: str, target_langs: List[str]) -> str:
        prompt = build_translation_prompt(text, current_lang, target_langs)
        # print("Prompt:\n", prompt)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        # print("AI Response:\n", response.output_text)
        return response.output_text # .choices[0].message.content.strip()

    def instruction_module(self, text: str, current_lang: str, target_langs: List[str]) -> str:
        prompt = build_instruction_prompt(text, current_lang, target_langs[0])
        # print("Prompt:\n", prompt)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        # print("AI Response:\n", response.output_text)
        return response.output_text # .choices[0].message.content.strip()
