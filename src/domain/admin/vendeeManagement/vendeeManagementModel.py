from pydantic import BaseModel,EmailStr
from typing import Union
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from ...models_domain.vendeeModel import  VendeeBase,VendeeBase,TujuanVendeeCategoryBase

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
    latitude : str | None = None
    longitude : str | None = None

# update vendee model
class UpdateDetailVendee(BaseModel) : 
    deskripsi : str | None = None
    work : str | None = None

class Updatevendee(BaseModelWithPhoneValidation) :
    username : str | None = None
    email : EmailStr | None = None
    no_telepon : str | None = None
    password : str | None = None

class UpdateAlamat(BaseModel) :
    village : str | None = None
    subdistrick : str | None = None
    regency : str | None = None
    province : str | None = None
    country : str | None = None
    latitude : str | None = None
    longitude : str | None = None

# search
class SearchVendee(BaseModel) :
    username : str | None = None
    online : bool | None = None

class SearchVendeeResponse(BaseModel) :
    vendee : list[VendeeBase]
    count_data : int
    count_page : int

# tujuan vendee category


class AddTujuanVendeeCategory(BaseModel) :
    id_tujuan_user_category : str
    isi : str

class UpdateTujuanVendeeCategory(BaseModel) :
    id_tujuan_user_category : Union[str,None] = None
    isi : Union[str,None] = None
