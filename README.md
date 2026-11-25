# ClauseIQ

ClauseIQ is a Streamlit application that uses Google's Gemini generative AI to analyze PDF and DOCX contracts. It extracts contract text and presents a structured summary, important clauses, potential risks, missing or weak clauses, obligations, dates, and recommendations.

## Requirements

- Python 3.10 or newer
- A Google Gemini API key

## Run locally

1. Clone this repository and open its folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your Gemini API key to `GEMINI_API_KEY`.
5. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Configuration

Set `GEMINI_API_KEY` in `.env`. `MODEL_NAME` is optional and defaults to `gemini-3.6-flash`.

## Privacy and use

Contract text is sent to the configured Gemini model for analysis. Do not upload documents unless you are authorized to share them with that service. ClauseIQ provides AI-generated information for review and is not a substitute for advice from a qualified lawyer.
