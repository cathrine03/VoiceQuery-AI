import re
from app.services.llm_client import client


SYSTEM_PROMPT = """
You are a PostgreSQL SQL generator.

Database schema:

sales(
    id,
    region,
    product,
    revenue,
    sale_date
)

Rules:
1. Return ONLY executable SQL.
2. Return exactly one SQL query.
3. Do not explain.
4. Do not think.
5. Do not output analysis.
6. Do not use markdown.
7. Do not use backticks.
8. SELECT statements only.
"""

def clean_sql(text: str):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.replace("```sql", "")
    text = text.replace("```", "")
    return text.strip()

def generate_sql(question: str):
    if not question or not question.strip():
        raise ValueError("Empty question received")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0,
    )

    if not question or not question.strip():
        return "SELECT 1;"

    raw = response.choices[0].message.content

    return clean_sql(raw)