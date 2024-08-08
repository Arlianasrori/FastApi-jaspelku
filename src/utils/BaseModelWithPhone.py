from pydantic import BaseModel,field_validator
from .phoneNumberValidation import phoneValidation


class BaseModelWithPhoneValidation(BaseModel) :
    no_telepon : str
    @field_validator("no_telepon",mode="before")
    def validate_no_telepon(cls, v) :
        return phoneValidation(v)