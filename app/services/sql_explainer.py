from app.services.llm_client import client

EXPLAIN_PROMPT = """
You are a data analyst.

Explain the SQL query in simple business language.

Keep the explanation:
- Short
- Clear
- Non-technical
- Maximum 3 sentences
"""

def explain_sql(sql: str):
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": EXPLAIN_PROMPT,
            },
            {
                "role": "user",
                "content": sql,
            },
        ],
        temperature=0,
    )

    if not sql or not sql.strip():
        return {"explanation": "No SQL generated yet."}

    return response.choices[0].message.content

    