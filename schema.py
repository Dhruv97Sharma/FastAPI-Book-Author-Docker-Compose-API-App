from pydantic import BaseModel
from typing import Union, Optional


class Book(BaseModel):
    title: Optional[str]
    rating: float
    author_id: Optional[int]
    price: Union[
        None,
        float
    ]
    unit_of_currency: Union[
       None,
       str
    ]

    class Config:
        orm_mode = True


class Author(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True
