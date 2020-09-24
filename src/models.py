from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class ToDo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(
        self,
        title: str,
        user_id: int,
        finished=False,
    ):
        self.title = title
        self.finished = finished
        self.user_id = user_id

    def update(self, title: str = None, finished: bool = None):
        if self.title == title and self.finished == finished:
            return

        if title is not None:
            self.title = title
        if finished is not None:
            self.finished = finished

        db.session.add(self)
        db.session.commit()
