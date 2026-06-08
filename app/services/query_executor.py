from sqlalchemy import text

from backend.app.db.session import SessionLocal


def execute_query(sql: str):
    db = SessionLocal()

    try:
        result = db.execute(text(sql))

        rows = []

        for row in result:
            rows.append(dict(row._mapping))

        return rows

    finally:
        db.close()