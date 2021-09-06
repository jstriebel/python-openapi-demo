* Install the project wiht [poetry](): `poetry install`
* Start the server: `poetry run uvicorn main:app --reload`
* Inspect the endpoints via their auto-generated docs:
  http://127.0.0.1:8000/docs
  http://127.0.0.1:8000/redoc
* Auto-test the server against its schema, using
  `poetry run schemathesis run http://127.0.0.1:8000/openapi.json`
* Fix the mistake it found (see `main.py` line 50)
* 
```

