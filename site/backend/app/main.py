from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_LOGIN = "admin"
TEMP_PASSWORD = "1234"

class LoginRequest(BaseModel):
    login: str
    password: str

@app.post("/api/login")
def login(data: LoginRequest):
    if data.login == TEMP_LOGIN and data.password == TEMP_PASSWORD:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="invalid credentials")
