from ..db.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

sessionDepedency = Annotated[Session,Depends(get_db)]