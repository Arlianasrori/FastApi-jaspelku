from pydantic import  BaseModel,EmailStr,Field,field_validator
from ...models.userModel import RoleUser
from ...utils.BaseModelWithPhone import BaseModelWithPhoneValidation

class RegisterBody(BaseModelWithPhoneValidation) :
    email: EmailStr
    no_telepon : str
    username : str = Field(max_length=255,min_length=4)
    password: str = Field(max_length=255,min_length=8)

    @field_validator("password")
    def validate_password(cls, v) :
        if " " in v :
            raise ValueError("passowrd tidak bisa mengandung spasi")
        return v     
    
class RegisterResponse(BaseModel) :
    id : str
    email: str
    username: str
    no_telepon : str
    access_token: str
    refresh_token: str


class LoginBody(BaseModel) :
    textBody : str | EmailStr
    password : str
    
class LoginResponse(BaseModel) :
    role: RoleUser | None 
    access_token: str
    refresh_token: str

class VerifyOTPBody(BaseModel) :
    OTP : str

class SelectRoleRequestBody(BaseModel) :
    role : RoleUser

class ResponseSelectRole(BaseModel) :
    id: str
    username: str
    email: EmailStr
    role: RoleUser

class ResponseVerifyTdTokenBeforeRegister(BaseModel) :
    email : EmailStr
    username : str

class ResponseGetUser(BaseModel) :
    id : str
    username : str
    isVerify : bool | None = None
    role : RoleUser | None = None

class ResponseRefreshToken(BaseModel) :
    access_token: str
    refresh_token: str
