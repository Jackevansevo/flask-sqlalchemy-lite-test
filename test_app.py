import pytest

from sqlalchemy import func, select
from app import User, db


@pytest.mark.usefixtures("app_ctx")
def test_a():
    user = User(name="test")
    db.session.add(user)
    db.session.commit()


@pytest.mark.usefixtures("app_ctx")
def test_b():
    assert db.session.scalar(select(func.count(User.id))) == 0
