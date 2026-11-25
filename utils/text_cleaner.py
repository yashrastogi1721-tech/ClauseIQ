import re


def clean_text(text):
    """
    Cleans extracted PDF text before sending it to the AI model.
    """

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text