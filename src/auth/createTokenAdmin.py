import os
from jose import JWTError, jwt

from ..error.errorHandling import HttpException


def create_token_admin(data) :
    try :
        ACCESS_KEY = os.getenv("ADMIN_SECRET_ACCESS_TOKEN")
        REFRESH_KEY = os.getenv("ADMIN_SECRET_REFRESH_TOKEN")
        access_token = jwt.encode(data,ACCESS_KEY,algorithm="HS256")
        refresh_token = jwt.encode(data,REFRESH_KEY,algorithm="HS256")
        return {"access_token" : access_token,"refresh_token" : refresh_token}
    except JWTError as Error:
        raise HttpException(status=400,message=Error.args)