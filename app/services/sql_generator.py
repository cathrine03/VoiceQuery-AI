import re
from ollama import chat


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
    text = text.replace("```sql", "").replace("```", "")
    return text.strip()


def generate_sql(question: str):
    response = chat(
        model="qwen2.5:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        options={
            "temperature": 0,
            "num_predict": 80,
        }
    )

    raw = response["message"]["content"]
    return clean_sql(raw)