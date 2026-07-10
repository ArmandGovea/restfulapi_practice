from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int | None = None
    is_read: bool = False


class BookCreate(BookBase):
    """What the client sends to create a book - no id yet"""

    pass


class BookUpdate(BaseModel):
    """All fields optional, since PATCH-style partial updates are allowed"""

    title: str | None = None
    author: str | None = None
    year: int | None = None
    is_read: bool | None = None


class BookResponse(BookBase):
    """What the api sends back - includes the id"""

    id: int

    class Config:
        from_attributes = True # lets pydantic read SQLAlchemy objects directly