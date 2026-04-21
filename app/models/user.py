from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    posts: list["Post"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")