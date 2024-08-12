from fastapi import Header,Request
from ...models.userModel import User
from ...error.errorHandling import HttpException
from ...utils.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
from sqlalchemy import select
import os

SECRET_KEY = os.getenv("USER_SECRET_ACCESS_TOKEN")

async def userAuthDepends(req : Request,Authorization: str = Header(default=None,example="jwt access token"),Session : sessionDepedency = None) :
    # get token from header with the bearer type 
    headerToken = Authorization

    if not headerToken :
        raise HttpException(status=401,message="invalid token(unauthorized)")
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

        if not findUser.__dict__["isVerify"] :
            raise HttpException(400,{"isVerify" : False,"msg" : "user belum melakukan verifikasi"})
        userDict = findUser.__dict__
        
        req.User = {
            "id" : userDict["id"],
            "username" : userDict["username"],
            "role" : userDict["role"]
        }
    except JWTError as error:
       raise HttpException(status=401,message=str(error.args[0])) 
