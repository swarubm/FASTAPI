from operator import index

from database import Base
from sqlalchemy import Integer, Column, Boolean,String


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    Complete = Column(Boolean,default=False)

