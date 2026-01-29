from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from database.db import get_db
from database.models import BoardORM, UserORM
from database.utils import hash_password, verify_password

router = APIRouter()