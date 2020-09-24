def test_register_user(client):
    res = client.post("/auth/register", json={"username": "my_user", "password": "baz"})
    assert res.status_code == 201
    assert res.get_json() == {"id": 3, "username": "my_user"}


def test_register_duplicate_user(client):
    res = client.post("/auth/register", json={"username": "user_1", "password": "baz2"})
    assert res.status_code == 400
    assert res.get_json() == {"error": "username already exists"}


def test_login(client):
    res = client.post("/auth/login", json={"username": "user_1", "password": "foo"})
    assert res.status_code == 200
    data = res.get_json()
    assert data.pop("token") is not None
    assert data == {"id": 1, "username": "user_1"}


def test_login_bad_user(client):
    res = client.post("/auth/login", json={"username": "user_111", "password": "foo"})
    assert res.status_code == 404
    assert res.get_json() == {"error": "user 'user_111' does not exist"}


def test_login_bad_password(client):
    res = client.post("/auth/login", json={"username": "user_1", "password": "foooo"})
    assert res.status_code == 401
    assert res.get_json() == {"error": "username or password is invalid"}
