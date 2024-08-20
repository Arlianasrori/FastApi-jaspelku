from pydantic import BaseModel,EmailStr
from typing import Union
from ...utils.BaseModelWithPhone import BaseModelWithPhoneValidation

class UserBase(BaseModelWithPhoneValidation) :
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str ,None] = None
    saldo : int

class AlamatBase(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str , None] = None
    longitude : Union[str , None] = None

class UpdateAlamat(BaseModel) :
    village : str | None = None
    subdistrick : str | None = None
    regency : str | None = None
    province : str | None = None
    country : str | None = None
    latitude : str | None = None
    longitude : str | None = None