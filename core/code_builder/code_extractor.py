import re
import re

def extract_code(text, language="python"):
    """
    Extracts code of the specified language from a text.

    If the text is already clean (no backticks), return it as a single code block.

    :param text: The text containing the code.
    :param language: The programming language of the code inside the backticks (default is "python").
    :return: List of extracted code snippets.
    """
    # If the text contains no code fences, assume it's already a clean code snippet
    if "```" not in text:
        return [text.strip()]
    
    # Regex pattern that matches code blocks with the specified language
    pattern = r'```' + re.escape(language) + r'\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)

    return [match.strip() for match in matches] if matches else [text.strip()]
