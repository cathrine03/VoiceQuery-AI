from ollama import chat

FIX_PROMPT = """
You are a PostgreSQL expert.

A SQL query failed.

Return ONLY corrected SQL.

Do not explain.
Do not use markdown.
"""


def fix_sql(
    question: str,
    sql: str,
    error: str
):
    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": FIX_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

SQL:
{sql}

Error:
{error}

Fix the SQL.
"""
            }
        ]
    )

    return (
        response["message"]["content"]
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )