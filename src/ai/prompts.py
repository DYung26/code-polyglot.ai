from typing import List

def build_translation_prompt(text: str, current_lang: str, target_langs: List[str]) -> str:
    langs_list = ', '.join(target_langs)
    return f"""
You are a multilingual code and documentation translator. Convert a document originally written with {current_lang} as its core language into the following target languages: {langs_list}.

The goal is to **adapt the whole document** (prose + code) to work in each target language.
If a direct translation is possible, do it. If not, like if it conveys something that is so {current_lang}-specific or a real-life story, provide a clear suggestion on how to achieve the same result in that language.

---

### Instructions:

1. **Prose**
   - Find any sentence, phrase, or explanation tied to {current_lang}'s way of thinking, including one-words.
   - Wrap it in:
     ```section
     …original prose…
     ```end
   - Directly below it, for each target language:
     ```<lang>
     Instruction or equivalent wording in <lang>.
     ```end

2. **Code**
   - Wrap every block of {current_lang} code in:
     ```{current_lang}
     …original code…
     ```end
   - Below each, include a full translation for each target language:
     ```<lang>
     …translated code…
     ```end

3. **General Rules**
   - Do not forget any fence - section, {current_lang}, etc...
   - You must return the **entire original document**, with translations inserted after each relevant section.
   - Do **not** modify text outside fenced sections.
   - Do **not** summarize or explain anything outside the required instructions.
   - Always resume the document on the next line after a fence.
   - Every code snippet, even within a prose instruction, **must** be translated or adapted.
   - Do the same for questions or quizzes too.

---

### Now follow the rules above and translate the document below:

_Current language_: {current_lang}
_Target languages_: {langs_list}

```text
{text}
````

Before submitting:

* Ensure every section is preserved and translated.
* No part of the original should be missing.
* Fences should be correctly formatted and complete.
  """

def build_instruction_prompt(
    translated_doc: str,
    original_lang: str,
    target_lang: str
) -> str:
    """
    Constructs a prompt that instructs the model to generate a structured translation instruction document
    based on an already-translated Snyk Learn module.

    Args:
        translated_doc: The text of the already-translated module.
        original_lang: The source language of the original module.
        target_lang: The language into which the module has been translated.

    Returns:
        A formatted prompt string ready for the model.
    """
    return f"""
INSTRUCTION:
*Include a link to the original module and indicate the translation {original_lang} → {target_lang} at the top.*

Instructions for Translation

1. Create a new Google Doc titled:
   Snyk Learn Module: {{vulnerability name}} translation instructions {original_lang} → {target_lang}

2. Copy all headings and subheadings from the original module.

3. For each subheading:
   - If code must change, write:
     Replace the code snippet in this section with the one below:
     {{new code snippet}}

   - If it’s an interactive step {{#}}, write:
     The code in step {{#}} should be replaced with:
     {{replacement code or text}}

   - If no change is needed, write:
     Nothing needs to be changed in this section.

4. Review: verify the document title format, all headings/subheadings,
   and that each section has clear instructions or notes.

5. Ensure every block of {target_lang} code is fenced in this format:
     ```{target_lang}
     …code…
     ```end
   Do not forget this.

---

NOW generate the **DONE TRANSLATION**–style instruction document from the translated module below:

Original language: {original_lang} → {target_lang}

Translated Module Text:
```text
{translated_doc}
```
"""

def build_instruction_conversion_prompt(instruction_text: str, current_lang: str, target_lang: str) -> str:
    return f"""Convert the following document that gives translation instructions from {current_lang} to {target_lang}.

Change all references, explanations, and code snippets accordingly. Preserve the structure and formatting.

--- START OF DOCUMENT ---

{instruction_text}

--- END OF DOCUMENT ---
"""
