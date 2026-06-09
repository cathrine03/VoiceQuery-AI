from app.services.llm_client import client

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
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": FIX_PROMPT,
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
""",
            },
        ],
        temperature=0,
    )

    return (
        response.choices[0]
        .message.content
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )