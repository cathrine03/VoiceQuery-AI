from ollama import chat

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
    response = chat(
        model="qwen2.5:3b",
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
        options={
            "temperature": 0,
            "num_predict": 120,
        },
    )

    return response["message"]["content"]