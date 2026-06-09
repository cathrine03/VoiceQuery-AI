import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_sql(sql: str):

    prompt = f"""
Explain this SQL query in simple terms:

SQL:
{sql}

Rules:
- Simple explanation
- No SQL rewriting
- No extra formatting
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You explain SQL clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return {
        "explanation": response.choices[0].message.content.strip()
    }