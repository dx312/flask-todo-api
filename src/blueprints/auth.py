from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from ..models import db, User
from ..utils import ApiResult, ApiException


bp = Blueprint("auth", __name__)


@bp.route("register", methods=["POST"])
def register_user():
    vars = request.get_json() or {}
    username = vars.get("username")
    password = vars.get("password")
    if not username or not password:
        raise ApiException("'username' and 'password' are required")
    if User.query.filter_by(username=username).first() is not None:
        raise ApiException("username already exists")
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return ApiResult({"id": user.id, "username": user.username}, 201)


@bp.route("login", methods=["POST"])
def login_user():
    vars = request.get_json() or {}
    username = vars.get("username")
    password = vars.get("password")
    if not username or not password:
        raise ApiException("'username' and 'password' are required")
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ApiException(f"user '{username}' does not exist", 404)
    autherized = user.check_password(password)
    if not autherized:
        raise ApiException("username or password is invalid", 401)
    token = create_access_token(user.id)
    return ApiResult({"token": token, "id": user.id, "username": username})
