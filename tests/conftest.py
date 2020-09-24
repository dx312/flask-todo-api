import pytest

from src.app import create_app
from src.models import db, User, ToDo


def populate_db():
    db.create_all()

    db.session.add(User("user_1", "foo"))
    db.session.add(User("user_2", "bar"))

    db.session.add(ToDo("Wake Up", user_id=1, finished=False))
    db.session.add(ToDo("Eat breakfast", user_id=1, finished=False))
    db.session.add(ToDo("Mow the lawn", user_id=2, finished=True))

    db.session.commit()


@pytest.fixture(scope="module")
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "super-secret-123",
        }
    )
    with app.app_context():
        populate_db()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()
