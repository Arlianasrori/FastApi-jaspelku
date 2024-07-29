from pydantic import BaseModel,EmailStr
from typing import Union

from datetime import datetime as DateTimetype
from ....models.servantModel import DayEnum
from ....models.pesananModel import Status_Pesanan_Enum

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

class PesananServant(BaseModel) :
    id : str
    processing_time : int
    datetime : DateTimetype
    additional_information : str
    order_estimate : str
    status : Status_Pesanan_Enum
    tugas : str
    total_price : int
    price_outside : int
    other_price : int
    isPay : bool
    approved : bool
    allowPayLater : bool
    isPayLater : bool
    detail_vendee : dict

class OrderServant(BaseModel) :
    id : str
    payment_using : str
    price : int
    dateTime : DateTimetype
    detail_vendee : dict
    pesanan : PesananServant

class MoreDetailServant(DetailServantBase) :
    tujuan_servant : TujuanServant | None = None
    jadwal_pelayanan : list[JadwalPelayananServant] | list= []
    time_servant : TimeServant | None = None 
    rating : int
    pesanans : list[PesananServant] | list = []
    orders : list[OrderServant] | list = []

class MoreServantBase(BaseModel) :
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    servant : MoreDetailServant 
    alamat : AlamatBase

class ServantBase(BaseModel) : 
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    servant : DetailServantBase 
    alamat : AlamatBase

class SearchServantResponse(BaseModel) :
    servant : list[ServantBase]
    count_data : int
    count_page : int

# add
class AddDetailservant(BaseModel) : 
    deskripsi : str
    id_pelayanan : str

class AddServant(BaseModel) :
    username : str
    email : EmailStr
    no_telepon : str
    password : str
    isVerify : bool = True

class AddAlamat(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

# update
class UpdateDetailservant(BaseModel) : 
    deskripsi : Union[str | None] = None
    id_pelayanan : Union[str | None] = None

class UpdateServant(BaseModel) :
    username : Union[str | None] = None

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