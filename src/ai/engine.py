from typing import List
from .client import get_client
from .prompts import build_translation_prompt


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

