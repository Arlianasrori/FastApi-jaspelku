from pydantic import BaseModel,EmailStr
from typing import Union
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from ...models_domain.vendeeModel import  VendeeBase,VendeeBase

# add vendee model
class AddDetailVendee(BaseModel) : 
    deskripsi : str

class AddVendee(BaseModelWithPhoneValidation) :
    username : str
    email : EmailStr
    no_telepon : str
    password : str
    isVerify : bool = True
    role : RoleUser = RoleUser.vendee

class AddAlamat(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

# update vendee model
class UpdateDetailVendee(BaseModel) : 
    deskripsi : Union[str | None] = None

class Updatevendee(BaseModelWithPhoneValidation) :
    username : Union[str | None] = None
    email : Union[EmailStr | None] = None
    no_telepon : str | None = None
    password : Union[str | None] = None

class UpdateAlamat(BaseModel) :
    village : Union[str | None] = None
    subdistrick : Union[str | None] = None
    regency : Union[str | None] = None
    province : Union[str | None] = None
    country : Union[str | None] = None
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

# search
class SearchVendee(BaseModel) :
    username : str | None = None
    online : bool | None = None

class SearchVendeeResponse(BaseModel) :
    vendee : list[VendeeBase]
    count_data : int
    count_page : int

# tujuan vendee category
class TujuanVendeeCategoryBase(BaseModel) :
    id : str
    id_tujuan_user_category : str
    isi : str

class AddTujuanVendeeCategory(BaseModel) :
    id_tujuan_user_category : str
    isi : str

class UpdateTujuanVendeeCategory(BaseModel) :
    id_tujuan_user_category : Union[str,None] = None
    isi : Union[str,None] = None
