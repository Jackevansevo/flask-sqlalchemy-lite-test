from __future__ import annotations

from flask import Flask
from flask_sqlalchemy_lite import SQLAlchemy

from datetime import datetime
from datetime import UTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db = SQLAlchemy()


class Model(DeclarativeBase):
    pass


class User(Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[list[Post]] = relationship(back_populates="author")


class Post(Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    author: Mapped[User] = relationship(back_populates="posts")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))


def create_app(test_config=None):
    app = Flask(__name__)
    app.config |= {"SQLALCHEMY_ENGINES": {"default": "sqlite:///default.sqlite"}}

    if test_config is None:
        app.config.from_prefixed_env()
    else:
        app.testing = True
        app.config |= test_config

    db.init_app(app)

    return app
