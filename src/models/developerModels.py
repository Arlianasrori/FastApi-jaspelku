from ..db.database import Base
from sqlalchemy import Column,String

class Developer(Base) :
    __tablename__ = "developer"

    username = Column(String,primary_key=True,unique=True,nullable=False)
    password = Column(String,nullable=False)