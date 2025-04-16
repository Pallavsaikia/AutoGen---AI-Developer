import re
def extract_code(text, language="python"):
    """
    Extracts code of the specified language from a text.

    :param text: The text containing the code.
    :param language: The programming language of the code inside the backticks (default is "python").
    :return: List of extracted code snippets.
    """
    # Regex pattern that matches code blocks with a specified language
    pattern = r'```' + re.escape(language) + r'\n(.*?)\n```'

    # Use re.DOTALL to allow matching multiline text
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the matched code
    return matches