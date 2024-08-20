from jose import jwt, JWTError
from sqlalchemy import select
import os
from ..models.userModel import User
from ..db.database import SessionLocal

SECRET_KEY = os.getenv("USER_SECRET_ACCESS_TOKEN")

async def auth_middleware(sid, environ,auth = {}):
    session = SessionLocal()
    try:
        auth_header = auth.get('access_token')
        if not auth_header:
            return False
        
        scheme, _, token = auth_header.partition(' ')
        
        if not token:
            return False
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if not payload:
                return False
            
            user_id = payload.get("id")
            
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            
            if not user or not user.isVerify:
                return False
            
            return {
                "user_id" : user_id,
            }
        except JWTError:
            return False
    finally:
        await session.close()
