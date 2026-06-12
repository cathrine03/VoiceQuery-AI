from app.services.sql_generator import (
    generate_sql
)

sql = generate_sql(
    "Show top products by revenue"
)

print(sql)