from pydantic import BaseModel,EmailStr
from typing import Union
from ....models.servantModel import DayEnum
from ..pesananOrderManagement.pesananOrderManagementModel import PesananBase,OrderBase
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation

# pelayanan servant
class AddPelayananServantCategory(BaseModel) :
    name : str

class UpdatePelayananServantCategory(BaseModel) :
    name : str

class ResponsePelayananServantCategory(BaseModel) :
    id : str 
    name : str

# servant
class AlamatBase(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

class PelayananServantBase(BaseModel) :
    id : str
    name : str

class TujuanServant(BaseModel) :
    id : str
    id_tujuan_servant_category : str
    tujuan_servant_category : dict

class JadwalPelayananServant(BaseModel) :
    id : str
    day : DayEnum

class TimeServant(BaseModel) :
    time : str

class DetailServantBase(BaseModel) :
    id : str
    id_servant : str
    deskripsi : str
    saldo : int
    ready_order : bool
    pelayanan : PelayananServantBase

class PesananServant(PesananBase) :
    detail_vendee : dict

class OrderServant(OrderBase) :
    pesanan : PesananServant

class MoreDetailServant(DetailServantBase) :
    tujuan_servant : TujuanServant | None = None
    jadwal_pelayanan : list[JadwalPelayananServant] | list= []
    time_servant : TimeServant | None = None 
    rating : int
    pesanans : list[PesananServant] | list = []
    orders : list[OrderServant] | list = []


class ServantBase(BaseModelWithPhoneValidation) : 
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    servant : DetailServantBase 
    alamat : AlamatBase

class MoreServantBase(ServantBase) :
    servant : MoreDetailServant 

# tujuan servant category
class TujuanServantCategoryBase(BaseModel) :
    id : str
    id_tujuan_user_category : str
    isi : str

# add
class AddDetailservant(BaseModel) : 
    deskripsi : str
    id_pelayanan : str

class AddServant(BaseModelWithPhoneValidation) :
    username : str
    email : EmailStr
    no_telepon : str
    password : str
    isVerify : bool = True
    role : str = RoleUser.servant

class AddAlamat(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

class AddTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : str
    isi : str

class UpdateTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : Union[str,None] = None
    isi : Union[str,None] = None

# update
class UpdateDetailservant(BaseModel) : 
    deskripsi : Union[str | None] = None
    id_pelayanan : Union[str | None] = None

class UpdateServant(BaseModelWithPhoneValidation) :
    username : Union[str | None] = None
    email : Union[EmailStr | None] = None
    no_telepon : str = None
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
class SearchServant(BaseModel) :
    username : str | None = None
    online : bool | None = None
    ready_order : bool | None = None

    model_config = {
        "json_schema": {
            "examples": [
                {
                    "username" : "habil",
                    "online": True,
                    "ready_order" : True
                }
            ]
        }
    }

class SearchServantResponse(BaseModel) :
    servant : list[ServantBase]
    count_data : int
    count_page : int