FORBIDDEN = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
]

def validate_sql(sql: str):
    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    for word in FORBIDDEN:
        if word in sql_lower:
            raise ValueError(f"Blocked unsafe SQL: {word}")