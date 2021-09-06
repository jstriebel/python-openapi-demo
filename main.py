from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="python-openapi-demo")
users: Dict[str, "User"] = {}


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None
    id: str


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    id: str


@app.post("/users/", response_model=UserOut)
async def create_user(user_input: UserIn):
    user_id = str(uuid4())
    user = User(
        username=user_input.username,
        password=user_input.password,
        email=user_input.email,
        full_name=user_input.full_name,
        id=user_id,
    )
    users[user_id] = user
    return user


@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: str):
    return users[user_id]  # better: users.get(user_id, None)


@app.get("/users/", response_model=List[UserOut])
async def read_users(n: Optional[int] = None):
    return list(users.values())[:n]


@app.get("/")
async def index():
    html_content = (
        f"""
    <html>
        <head>
            <title>OpenApi-Demo-Server</title>
        </head>
        <body>
            <h1>Docs</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
                <li><a href="/openapi.json">/openapi.json</a></li>
            </ul>
            <h1>User State</h1>
            <ul>
            {''.join('<li>' + user.username + '</li>' for user in users.values())}
            </ul>
            <button id="adduser">add dummy user</button>
        </body>
"""
        + """
        <script>
            var adduser = document.querySelector("#adduser");
            adduser.onclick = async (e) => {
                const response = await fetch('/users/', {
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({username: 'dummy' + Math.floor(Math.random() * 10), password: '***', email: 'dummy@mail.org'}),
                });
                location.reload();
            };
        </script>
    </html>
    """
    )
    return HTMLResponse(content=html_content, status_code=200)
