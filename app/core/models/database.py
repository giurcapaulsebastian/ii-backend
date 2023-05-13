import random
from datetime import datetime

from sqlalchemy import Float, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from passlib import hash
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_number = Column(String, index=True, unique=True)
    status = Column(String, index=True, default="created")
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    user = relationship("User", back_populates="orders")

    @staticmethod
    def generate_order_number():
        now = datetime.now()
        rand_num = random.randint(10000, 99999)
        return f"{now.strftime('%Y%m%d%H%M%S')}-{rand_num}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_number = self.generate_order_number()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OrderProducts(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


Order.order_products = relationship("OrderProducts", back_populates="order")
Product.order_products = relationship("OrderProducts", back_populates="product")
