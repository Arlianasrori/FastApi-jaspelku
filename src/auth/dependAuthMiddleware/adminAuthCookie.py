from fastapi import Cookie, Request

from ...models.developerModels import Developer
from ...error.errorHandling import HttpException
from ...utils.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

SECRET_KEY = os.getenv("ADMIN_SECRET_ACCESS_TOKEN")

async def adminCookieAuth(access_token : str | None = Cookie("access_token"),req : Request = None,Session : sessionDepedency = None) :
    print(access_token)
    if not access_token :
        raise HttpException(status=401,message="invalid token(unauthorized)")
    try :
        admin = jwt.decode(access_token,SECRET_KEY,algorithms="HS256")

        if not admin :
            raise HttpException(status=401,message="invalid token(unauthorized)")
        
        selectQuery = select(Developer.username).where(Developer.username == admin["sub"])
        exec = await Session.execute(selectQuery)
        findAdmin = exec.first()

        if not findAdmin : 
            raise HttpException(status=401,message="invalid token(unauthorized)")
        req.admin = findAdmin._asdict()
    except JWTError as error:
       raise HttpException(status=401,message=str(error.args[0])) 
