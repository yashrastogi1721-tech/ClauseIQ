import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.6-flash")

model = genai.GenerativeModel(MODEL_NAME)


def analyze_contract(contract_text):
    """
    Sends the contract text to Gemini and returns
    a structured JSON-style analysis.
    """

    prompt = f"""
You are an AI legal contract analysis assistant.

Analyze the contract provided below.

IMPORTANT RULES:

1. Use ONLY information explicitly present in the contract.
2. Do not invent facts, clauses, dates, parties, or obligations.
3. If information is not present, write "Not Mentioned".
4. Do not provide definitive legal advice.
5. Identify potential risks and explain why they may be risky.
6. Return ONLY valid JSON.
7. Do not use Markdown.
8. Do not put the JSON inside ```json or ``` code blocks.

Return the analysis using EXACTLY this structure:

{{
    "executive_summary": "Brief summary of the contract",

    "important_clauses": [
        {{
            "clause_name": "Name of clause",
            "description": "What the clause says",
            "importance": "Why this clause is important"
        }}
    ],

    "risky_clauses": [
        {{
            "clause_name": "Name of clause",
            "risk_level": "Low/Medium/High",
            "description": "What the clause says",
            "risk_reason": "Why this may create a risk"
        }}
    ],

    "missing_or_weak_clauses": [
        {{
            "clause_name": "Clause name",
            "reason": "Why it appears missing or weak"
        }}
    ],

    "obligations": [
        {{
            "party": "Party name",
            "obligation": "What the party is required to do"
        }}
    ],

    "important_dates": [
        {{
            "date": "Date or deadline",
            "event": "What happens on this date"
        }}
    ],

    "overall_risk": "Low/Medium/High",

    "risk_score": 0,

    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}}

The risk_score must be an integer between 0 and 100.

Contract:

{contract_text}
"""

    try:
        response = model.generate_content(prompt)

        response_text = response.text.strip()

        analysis = json.loads(response_text)

        return analysis

    except json.JSONDecodeError:
        return {
            "error": "Gemini returned invalid JSON."
        }

    except Exception as e:
        return {
            "error": str(e)
        }