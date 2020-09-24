import os
from typing import Dict

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .blueprints.api import bp as api_bp
from .blueprints.auth import bp as auth_bp
from .models import db
from .utils import ApiException, ApiResult


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            return rv.to_response()
        return super().make_response(rv)


def create_app(config: Dict[str, str] = None) -> ApiFlask:
    app = ApiFlask("api")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", 0)
    )
    app.config.update(config or {})
    Bcrypt(app)
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_error_handler(ApiException, lambda err: err.to_result())
    return app
