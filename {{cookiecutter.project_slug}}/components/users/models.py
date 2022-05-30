from sqlalchemy import Boolean, Column, Integer, String

from components.core.models import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # items = relationship("Product", back_populates="owner")
