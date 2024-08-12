from operator import itemgetter
from pydantic import BaseModel,EmailStr, Field, field_validator
from typing import Union
from ...models.servantModel import DayEnum
from .pesananOrderModel import PesananBase,OrderBase,PesananVendee
from ...utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from .userModel import AlamatBase

class PelayananServantBase(BaseModel) :
    id : str
    name : str

class TujuanServant(BaseModel) :
    id : str
    id_tujuan_servant_category : str
    tujuan_servant_category : dict

    @field_validator("tujuan_servant_category",mode="before")
    def validate_no_telepon(cls, v) :
        k = v.__dict__
        k.pop("_sa_instance_state")
        return k

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
    pass_test : bool
    pelayanan : PelayananServantBase

class PesananServant(PesananBase) :
    detail_vendee : PesananVendee

class OrderServant(OrderBase) :
    pesanan : PesananServant

class MoreDetailServant(DetailServantBase) :
    tujuan_servant : TujuanServant | None = None
    jadwal_pelayanan : list[JadwalPelayananServant] = []
    time_servant : TimeServant | None = None 
    rating : int
    pesanans : list[PesananServant] = []
    orders : list[OrderServant] = []
class DetailServantWithoutRatingPesananOrder(DetailServantBase) :
    tujuan_servant : TujuanServant | None = None
    jadwal_pelayanan : list[JadwalPelayananServant] = []
    time_servant : TimeServant | None = None 
    
class ServantBase(BaseModelWithPhoneValidation) : 
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    servant : DetailServantBase 
    alamat : AlamatBase | None = None

class MoreServantBase(ServantBase) :
    servant : MoreDetailServant 

# tujuan servant category
class TujuanServantCategoryBase(BaseModel) :
    id : str
    id_tujuan_user_category : str
    isi : str