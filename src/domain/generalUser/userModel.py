from pydantic import BaseModel, EmailStr, field_validator

class ResponseUpdateFotoProfile(BaseModel):
    id: str
    username: str
    email: str
    no_telepon: str
    foto_profile: str

class VerifyOtpForPasswordEmail(BaseModel):
    OTPcode: str

class UpdatePassword(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if " " in v:
            raise ValueError("password tidak bisa mengandung spasi")
        return v

class ResponsePassword(BaseModel):
    msg: str

class UpdateEmail(BaseModel):
    email: EmailStr

class ResponseEmail(BaseModel):
    id: str
    email: str
    username: str
    no_telepon: str

class ResponseUpdateIsOnline(BaseModel):
    id_user: str
    online: bool