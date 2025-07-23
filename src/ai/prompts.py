from typing import List

def build_translation_prompt(text: str, target_langs: List[str]) -> str:
    langs_list = ', '.join(target_langs)
    return f"""
You are an expert polyglot code translator. I will give you a document containing prose and code blocks. Note: the code blocks may or may not be properly formatted using backticks—your task is to identify all blocks of code in the document, even if they are not explicitly fenced.

Your task is:

1. For each identifiable code block in the document:
   - Leave the original block exactly as‑is.
   - Immediately append a translated version for each of these target languages (in the order given): {langs_list}
   - Use this exact fence format for each translation:

     ```<lang>
     // translated code here
     ```end

   where `<lang>` is one of: cpp, csharp, go, js, python, php, java (only those present in the target list).

2. Do not modify any narrative text or original code blocks.
3. Do not add explanations or commentary—output only the full document with appended translations.

**Example**

Target languages: go, python

_Input Document_:
Here’s a small example:

function add(a, b) {{
  return a + b;
}}

Done.

*Expected Output*:

````
Here’s a small example:

```js
function add(a, b) {{
  return a + b;
}}
```end
```go
func add(a int, b int) int {{
    return a + b
}}
```end
```python
def add(a, b):
    return a + b
```end

Done.
````

Now, translate this document:

Target languages: {langs_list}

Document:

```
{text}
```

"""
