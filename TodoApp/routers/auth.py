from typing import Annotated

from fastapi import APIRouter, Depends
from opentelemetry.trace import Status
from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status

from database import sessionLocal
from models import Users
from passlib.context import CryptContext


router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')





class CreateRequest(BaseModel):
    username:str
    first_name:str
    last_name: str
    email:str
    password:str
    role: str

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



@router.post("/auth/",status_code=status.HTTP_201_CREATED)

async def create_user( db:db_dependency,create_user_request:CreateRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    return create_user_model
    # return{'user':'authenticated'}
