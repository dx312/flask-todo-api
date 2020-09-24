from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import db, ToDo
from ..utils import ApiResult, ApiException


bp = Blueprint("api", __name__)


@bp.route("/todos", methods=["GET"])
@jwt_required
def get_todos():
    user_id = get_jwt_identity()
    todos = ToDo.query.filter_by(user_id=user_id).all()
    data = []
    for todo in todos:
        data.append(
            {
                "id": todo.id,
                "title": todo.title,
                "finished": todo.finished,
            }
        )
    return ApiResult({"todos": data})


@bp.route("/todos", methods=["POST"])
@jwt_required
def create_todo():
    vars = request.get_json() or {}
    title = vars.get("title")
    if not title:
        raise ApiException("'title' is required")
    user_id = get_jwt_identity()
    todo = ToDo(
        title=title,
        finished=False,
        user_id=user_id,
    )
    db.session.add(todo)
    db.session.commit()
    return ApiResult(
        {
            "id": todo.id,
            "title": todo.title,
            "finished": todo.finished,
        },
        201,
    )


@bp.route("/todos/<int:todo_id>", methods=["PUT"])
@jwt_required
def update_todo(todo_id: int):
    user_id = get_jwt_identity()
    todo = ToDo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        raise ApiException(f"todo with id '{todo_id}' not found", 404)

    vars = request.get_json() or {}
    title = vars.get("title")
    finished = vars.get("finished")
    todo.update(title, finished)
    return ApiResult(
        {
            "id": todo.id,
            "title": todo.title,
            "finished": todo.finished,
        }
    )


@bp.route("/todos/<int:todo_id>", methods=["DELETE"])
@jwt_required
def delete_todo(todo_id: int):
    user_id = get_jwt_identity()
    todo = ToDo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        raise ApiException(f"todo with id '{todo_id}' not found", 404)
    db.session.delete(todo)
    db.session.commit()
    return ApiResult({"deleted": todo_id})
