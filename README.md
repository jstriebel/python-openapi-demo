# Python OpenAPI Demo

Demo Project showcasing OpenAPI usage in Python via [FastAPI](https://fastapi.tiangolo.com/), [Schemathesis](https://schemathesis.readthedocs.io/) & [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)

* Prerequisites: Python 3.7+ and [Poetry](https://python-poetry.org/docs/#installation)
* Install the project: `poetry install`
* Start the server: `poetry run uvicorn main:app --reload`
  and explore http://127.0.0.1:8000
* Inspect the REST API via their auto-generated docs:
  http://127.0.0.1:8000/docs
  http://127.0.0.1:8000/redoc
* Auto-test the (still running) server against its schema, using
  `poetry run schemathesis run http://127.0.0.1:8000/openapi.json`
  and fix the mistake it found if you like (see `main.py` line 50)
* Generate a Python client from the server's OpenAPI definitions and try it out:
  ```bash
  poetry run openapi-python-client generate --url http://127.0.0.1:8000/openapi.json
  # maybe restart the server now to get rid of the user entries from schemathesis
  cd python-openapi-demo-client
  poetry install
  poetry run python
  ```
  In the Python REPL, run:
  ```python
  from python_openapi_demo_client import Client
  from python_openapi_demo_client.api.default import create_user_users_post, read_users_users_get
  from python_openapi_demo_client.models import UserIn

  client = Client(base_url="http://127.0.0.1:8000")

  test_user = create_user_users_post.sync(
      client=client,
      json_body=UserIn(
          username="test-user",
          password="***",
          email="test-user@mail.org"
      )
  )
  print(test_user)
  all_users = read_users_users_get.sync(client=client)
  assert test_user in all_users
  print(read_users_users_get.sync(client=client, n=3))
  ```
