from watchfiles import awatch
from ..db.database import SessionLocal,engine
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
async def get_db():
    # async with engine.begin() as conn :
    #     await conn.()
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

sessionDepedency = Annotated[Session,Depends(get_db)]