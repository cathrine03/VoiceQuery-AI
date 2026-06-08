from sqlalchemy import Column, Integer, String, Float, Date

from app.db.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    region = Column(String, nullable=False)

    product = Column(String, nullable=False)

    revenue = Column(Float, nullable=False)

    sale_date = Column(Date, nullable=False)