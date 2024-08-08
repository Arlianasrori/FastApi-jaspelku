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


class LoginBody(RegisterBody) :
    textBody : str | EmailStr
    password : str
    
class LoginResponse(BaseModel) :
    role: RoleUser
    acces_token: str
    refresh_token: str