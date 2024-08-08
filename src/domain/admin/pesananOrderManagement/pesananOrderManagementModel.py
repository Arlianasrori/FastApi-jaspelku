from ....models.pesananModel import Status_Pesanan_Enum
from pydantic import BaseModel, EmailStr,field_validator
from datetime import date as Datetype,time as Timetype
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from typing import Union

class PesananBase(BaseModel) :
    id : str
    date : Datetype | None = None
    time : Timetype | None = None
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

class OrderBase(BaseModel) :
    id : str
    payment_using : str
    price : int
    date : Datetype | None = None
    time : Timetype | None = None

class UserBase(BaseModelWithPhoneValidation) :
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str | None] = None

class PesananServant(BaseModel) :
    id : str
    id_servant : str
    deskripsi : str
    saldo : int
    ready_order : bool
    pelayanan : dict | None 
    servant : UserBase

    @field_validator("pelayanan", mode="before")
    @classmethod
    def transform(cls, raw: str) -> tuple[int, int]:
        if not raw :
            return None
        return {
            "id" : raw.__dict__["id"],
            "name" : raw.__dict__["name"]
        }

    class Config:
        arbitrary_types_allowed = True

class PesananVendee(BaseModel) :
    id : str
    id_vendee : str
    deskripsi : Union[str,None] = None
    saldo : int
    vendee : UserBase

class PesananWithVendeeServant(PesananBase) :
    detail_servant : PesananServant
    detail_vendee : PesananVendee

class OrdernWithVendeeServant(OrderBase) :
    detail_servant : PesananServant
    detail_vendee : PesananVendee
    pesanan : PesananBase

class SearchPesananOrder(BaseModel) :
    servant : Union[str | None] = None
    vendee : Union[str | None] = None
    tugas : Union[str | None] = None
    year : Union[int | None] = None
    month : Union[int | None] = None
    day : Union[int | None] = None

class StatisticPesanan(BaseModel) :
    total_pesanan : int
    jumlah_pesanan_pengajuan : int 
    jumlah_pesanan_proses : int
    jumlah_pesanan_dibatalkan_vendee : int
    jumlah_pesanan_dibatalkan_servant : int
    jumlah_pesanan_selesai : int
    total_pendapatan_from_pesanan : int

    @field_validator("total_pendapatan_from_pesanan",mode="before")
    def settotal_pendapatan_from_pesanan(cls, v):
        return v if v else 0

class StatisticOrder(BaseModel) :
    total_order : int
    jumlah_order_bni : int
    total_price : int

class SearchPesananResponse(BaseModel) :
    pesanans : list[PesananWithVendeeServant]
    count_data : int
    count_page : int

class SearchOrderResponse(BaseModel) :
    orders : list[OrdernWithVendeeServant]
    count_data : int
    count_page : int

class ResponseOverviewPesanan(BaseModel) :
    januari : StatisticPesanan 
    februari : StatisticPesanan 
    maret : StatisticPesanan 
    april : StatisticPesanan 
    mei : StatisticPesanan 
    juni : StatisticPesanan 
    juli : StatisticPesanan 
    agustus : StatisticPesanan 
    september : StatisticPesanan 
    oktober : StatisticPesanan 
    november : StatisticPesanan 
    desember : StatisticPesanan 

class ResponseOverviewOrder(BaseModel) :
    januari : StatisticOrder 
    februari : StatisticOrder 
    maret : StatisticOrder 
    april : StatisticOrder 
    mei : StatisticOrder 
    juni : StatisticOrder 
    juli : StatisticOrder 
    agustus : StatisticOrder 
    september : StatisticOrder 
    oktober : StatisticOrder 
    november : StatisticOrder 
    desember : StatisticOrder 