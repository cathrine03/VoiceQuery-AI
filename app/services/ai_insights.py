from backend.app.core.groq_client import client

INSIGHT_PROMPT = """
You are a senior data analyst.

You are given:
- A user question
- SQL query
- Query results (JSON)

Your job:
Generate business insights.

Rules:
- ONLY insights
- Max 5 bullet points
- Focus on trends, patterns, anomalies
- Do NOT explain SQL
- Do NOT repeat raw data
- Keep it concise and executive-friendly
"""

def generate_insights(question: str, sql: str, results: list):

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": INSIGHT_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

SQL:
{sql}

Results:
{results}
""",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content