import pytest


@pytest.fixture(scope="module")
def headers(client):
    res = client.post("/auth/login", json={"username": "user_1", "password": "foo"})
    assert res.status_code == 200
    return {"Authorization": "Bearer " + res.get_json()["token"]}


def test_get_todos(client, headers):
    res = client.get("/api/todos", headers=headers)
    assert res.status_code == 200
    assert res.get_json() == {
        "todos": [
            {
                "id": 1,
                "title": "Wake Up",
                "finished": False,
            },
            {
                "id": 2,
                "title": "Eat breakfast",
                "finished": False,
            },
        ]
    }


def test_create_todo(client, headers):
    res = client.post(
        "/api/todos",
        json={"title": "A new todo"},
        headers=headers,
    )
    assert res.status_code == 201
    assert res.get_json() == {
        "id": 4,
        "title": "A new todo",
        "finished": False,
    }

    # make sure the todo was created for the correct user
    res = client.get("/api/todos", headers=headers)
    assert len(res.get_json()["todos"]) == 3


def test_update_todo(client, headers):
    res = client.put("/api/todos/4", json={"finished": True}, headers=headers)
    assert res.status_code == 200
    assert res.get_json() == {
        "id": 4,
        "finished": True,
        "title": "A new todo",
    }


def test_delete_todo(client, headers):
    res = client.delete("/api/todos/4", headers=headers)
    assert res.status_code == 200
    assert res.get_json() == {"deleted": 4}

    # make sure the todo was deleted for the correct user
    res = client.get("/api/todos", headers=headers)
    assert len(res.get_json()["todos"]) == 2
