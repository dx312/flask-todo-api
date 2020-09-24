# A Simple Flask-Postgres ToDo API

## Quickstart

Create a `.env` file in the root of the repo with keys

- JWT_SECRET_KEY
- FLASK_ENV
- FLASK_DEBUG

launch the postgres db with flask api server

```bash
docker-compose up
```

register a new user

```bash
curl -X POST -H "Content-Type: application/json" \
 -d '{"username": "dev", "password": "secret123"}' \
 https://localhost:5000/auth/register
```

login and receive a token

```bash
curl -X POST -H "Content-Type: application/json" \
 -d '{"username": "dev", "password": "secret123"}' \
 https://localhost:5000/auth/login
```

create a todo (replace <token> with your token)

```bash
curl -X POST -H "Content-Type: application/json; Authorization: Bearer <token>" \
 -d '{"todo": "take a nap"}' \
 https://localhost:5000/api/todos
```

get all of your todos (replace <token> with your token)

```bash
curl -X GET -H "Content-Type: application/json; Authorization: Bearer <token>" \
 https://localhost:5000/api/todos
```

update a todo (replace <token> and <todo-id>)

```bash
curl -X PUT -H "Content-Type: application/json; Authorization: Bearer <token>" \
 -d '{"title": "take a short nap", "finished": "true"}' \
 https://localhost:5000/api/todos/<todo-id>
```

delete a todo (replace <token> and <todo-id>)

```bash
curl -X DELETE -H "Content-Type: application/json; Authorization: Bearer <token>" \
 -d '{"title": "take a short nap", "finished": "true"}' \
 https://localhost:5000/api/todos/<todo-id>
```

## Development

Setup a local dev enviroment with [pipenv](https://pipenv.pypa.io/en/latest/).

```bash
pipenv install --dev --pre
```

Linting

```bash
make lint
```

Formating

```bash
make format
```

Tests

```bash
make tests
```
