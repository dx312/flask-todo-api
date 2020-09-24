from flask_script import Manager

from src.app import create_app
from src.models import db


manager = Manager(create_app)


@manager.command
def createdb(drop_first=False):
    db.create_all()
