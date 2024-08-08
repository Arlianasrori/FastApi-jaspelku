from fastapi import Request
from ..models.userModel import User
from ..error.errorHandling import HttpException
from ..utils.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

SECRET_KEY = os.getenv("USER_SECRET_ACCESS_TOKEN")

async def userAuthDepends(req : Request = None,Session : sessionDepedency = None) :
    # get token from header with the bearer type 
    headerToken = req.headers.get("Authorization")
    # split token fdrom header token,and get in array 1
    access_token = headerToken.split(" ")[1]
    print(access_token)
    if not access_token :
        raise HttpException(status=401,message="invalid token(unauthorized)")
    try :
        # decode jwt token
        user = jwt.decode(access_token,SECRET_KEY,algorithms="HS256")

        if not user :
            raise HttpException(status=401,message="invalid token(unauthorized)")
        
        selectQuery = select(User).where(User.id == user["id"])
        exec = await Session.execute(selectQuery)
        findUser = exec.scalars().first()

        if not findUser : 
            raise HttpException(status=401,message="invalid token(unauthorized)")
        req.user = {
            "id" : findUser["id"],
            "username" : findUser["username"],
            "role" : findUser["role"]
        }
    except JWTError as error:
       raise HttpException(status=401,message=error.args) 
