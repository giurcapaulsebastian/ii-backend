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

