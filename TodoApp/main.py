from fastapi import FastAPI,Depends
import models
from TodoApp.models import Todos
from database import engine,sessionLocal
from  typing import  Annotated
from sqlalchemy.orm import session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated([session,Depends(get_db)])
@app.get("/")
async def read_all(db:db_depencency):
    return db.query(Todos).all()

