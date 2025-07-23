from typing import List, Tuple

def get_index_of_line_start(document: dict, line_number: int) -> int:
    """
    Returns the character index of the start of the given line (0-based).
    Raises IndexError if the line_number is out of range.
    """
    lines = []
    current_index = 1  # Google Docs starts counting at 1

    for element in document.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue

        paragraph_elements = paragraph.get("elements", [])
        for el in paragraph_elements:
            content = el.get("textRun", {}).get("content", "")
            if content:
                split_lines = content.splitlines(keepends=True)
                for line in split_lines:
                    lines.append((current_index, line))
                    current_index += len(line)

    print(line_number, len(lines))
    if line_number < len(lines):
        return lines[line_number][0]
    elif len(lines) == 0 and line_number == 0:
        return 1  # start of empty doc
    else:
        raise IndexError("Requested line number out of range.")

def find_backtick_lines(text: str) -> List[Tuple[int, str]]:
    """
    Return a list of (line_number, line_content) for lines that start with ```.

    line_number is 0-based (so 0 is the first line).
    """
    result: List[Tuple[int, str]] = []
    for i, line in enumerate(text.splitlines()):
        stripped = line.lstrip()  # allow leading spaces
        if stripped.startswith("```"):
            result.append((i, stripped))  # store the trimmed content
    return result

LANGUAGE_COLORS = {
    "cpp": {"red": 0.0, "green": 0.5, "blue": 0.8},         # bluish cyan
    "csharp": {"red": 0.5, "green": 0.0, "blue": 0.5},      # purple (from .NET branding)
    "go": {"red": 0.0, "green": 0.0, "blue": 1.0},          # blue (Go gopher)
    "js": {"red": 1.0, "green": 1.0, "blue": 0.0},          # yellow (JS branding)
    "javascript": {"red": 1.0, "green": 1.0, "blue": 0.0},  # alias for "js"
    "python": {"red": 0.0, "green": 0.6, "blue": 0.0},      # greenish (from its snake-like logo palette)
    "php": {"red": 0.4, "green": 0.0, "blue": 0.8},         # deep purple (PHP branding)
    "java": {"red": 1.0, "green": 0.3, "blue": 0.0},        # orange-red (coffee logo color)
}
