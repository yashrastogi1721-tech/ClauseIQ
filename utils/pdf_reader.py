import fitz


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from every page of a PDF uploaded through Streamlit.
    """

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text
