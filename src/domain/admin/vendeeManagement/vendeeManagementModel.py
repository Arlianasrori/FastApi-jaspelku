from pydantic import BaseModel,EmailStr
from typing import Union
from ..pesananOrderManagement.pesananOrderManagementModel import PesananBase,OrderBase
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation

class AlamatBase(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

class PesananVendee(PesananBase) :
    detail_servant : dict

class OrderVendee(OrderBase) :
    pesanan : PesananVendee

class DetailVendeeBase(BaseModel) :
    id : str
    id_vendee : str
    deskripsi : Union[str,None] = None
    saldo : int

class MoreDetailVendee(DetailVendeeBase) :
    pesanans : Union[list[PesananVendee] | list] = []
    orders  : Union[list[OrderVendee] | list] = []

class VendeeBase(BaseModelWithPhoneValidation) : 
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    vendee : DetailVendeeBase 
    alamat : AlamatBase

class MoreVendee(VendeeBase) :
    vendee : MoreDetailVendee

# add vendee model
class AddDetailVendee(BaseModel) : 
    deskripsi : str

class AddVendee(BaseModelWithPhoneValidation) :
    username : str
    email : EmailStr
    no_telepon : str
    password : str
    isVerify : bool = True
    role : str = RoleUser.vendee

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
