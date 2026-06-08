from datetime import date
from random import choice, randint

from app.db.session import SessionLocal
from app.db.models.sales import Sale

db = SessionLocal()

regions = [
    "North",
    "South",
    "East",
    "West"
]

products = [
    "Laptop",
    "Phone",
    "Tablet",
    "Monitor"
]

for _ in range(50):
    sale = Sale(
        region=choice(regions),
        product=choice(products),
        revenue=randint(1000, 15000),
        sale_date=date(
            2025,
            randint(1, 12),
            randint(1, 28)
        )
    )

    db.add(sale)

db.commit()

print("Sales data inserted successfully")