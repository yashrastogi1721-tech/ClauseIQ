from docx import Document


def extract_text_from_docx(uploaded_file):
    """
    Extracts text from an uploaded DOCX file.
    """

    document = Document(uploaded_file)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)