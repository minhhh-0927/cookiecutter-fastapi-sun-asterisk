from typing import Union

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
