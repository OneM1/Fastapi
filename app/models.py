from typing import List, Optional
from datetime import datetime
from sqlmodel import TIMESTAMP, Column, Field, ForeignKey, SQLModel, text
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True)
    created_at: datetime = Field(
sa_column=Column(
TIMESTAMP(timezone=True),
nullable=False,
server_default=text("CURRENT_TIMESTAMP"),
server_onupdate=text("CURRENT_TIMESTAMP")
)
)
    owner_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
        )
    )
    # Relationship: A post belongs to a user
    owner: Optional["Users"] = Relationship(back_populates="posts")
    votes: List["Votes"] = Relationship(back_populates="post")

class Users(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    email:str=Field(nullable=False,unique=True)
    username:str=Field(nullable=False,unique=True)
    password:str=Field(nullable=False)
    created_at: datetime = Field(
    sa_column=Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=text("CURRENT_TIMESTAMP"),
    server_onupdate=text("CURRENT_TIMESTAMP")
)
)
    phone_number:int = Field(nullable=True)
    posts: list["Posts"] = Relationship(back_populates="owner")
    votes: List["Votes"] = Relationship(back_populates="user")


class Votes(SQLModel, table=True):
    post_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            "post_id",
            ForeignKey("posts.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    user_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            "user_id",
            ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    post: "Posts" = Relationship(back_populates="votes")
    user: "Users" = Relationship(back_populates="votes")