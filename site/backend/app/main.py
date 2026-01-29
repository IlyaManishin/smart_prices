from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routers.api import router as api_router 
from routers.board_host import router as brd_router

from core import init_users
from database import db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db.init_db()
init_users.init_admin_user()

app.include_router(api_router, prefix="/api")
app.include_router(brd_router, prefix="/board_host")

app.mount("/", StaticFiles(directory="front", html=True), name="frontend")
