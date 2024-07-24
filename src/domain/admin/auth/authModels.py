from pydantic import BaseModel

class LoginModel(BaseModel) :
    username : str
    password : str

class ResponseLoginAdmin(BaseModel) :
    access_token : str
    refresh_token : str