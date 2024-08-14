from watchfiles import awatch
from ..db.database import SessionLocal,engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
async def get_db():
    # async with engine.begin() as conn :
    #     await conn.()
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

sessionDepedency = Annotated[AsyncSession,Depends(get_db)]