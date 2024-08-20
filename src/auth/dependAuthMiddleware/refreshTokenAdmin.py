from fastapi import Cookie, Request

from ...models.developerModels import Developer
from ...error.errorHandling import HttpException
from ...utils.sessionDepedency import sessionDepedency
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("ADMIN_SECRET_REFRESH_TOKEN")

def refresh_token_auth(refresh_token : str | None = Cookie(None),req : Request = None,Session : sessionDepedency = None) :
    print(refresh_token)
    if not refresh_token :
        raise HttpException(status=401,message="invalid token(unauthorized)")
    try :
        admin = jwt.decode(refresh_token,SECRET_KEY,algorithms="HS256")

        if not admin :
            raise HttpException(status=401,message="invalid token(unauthorized)")
        
        findAdmin = Session.query(Developer.username).where(Developer.username == admin["sub"]).one()

        if not findAdmin : 
            raise HttpException(status=401,message="invalid token(unauthorized)")
        req.refresh_admin = findAdmin._asdict()
    except JWTError as error:
       raise HttpException(status=401,message=error.args) 
