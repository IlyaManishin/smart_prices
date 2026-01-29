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

@app.get("/api/boards")
def get_boards():
    return [
        {
            "id": 1,
            "product": "Молоко ультрапастеризованное 3.2% 1 литр",
            "base_price": 129.90,
            "discount": 10,
            "installed_at": "2026-01-20",
            "synced": True
        },
        {
            "id": 2,
            "product": "Хлеб ржаной фермерский нарезной",
            "base_price": 54.50,
            "discount": 0,
            "installed_at": "2026-01-18",
            "synced": False
        }
    ]