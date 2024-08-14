from ...models.pesananModel import Status_Pesanan_Enum
from pydantic import BaseModel,field_validator
from datetime import date as Datetype,time as Timetype
from typing import Union
from .userModel import UserBase

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
    approved : bool | None = None

class OrderBase(BaseModel) :
    id : str
    payment_using : str
    price : int
    date : Datetype | None = None
    time : Timetype | None = None

class PesananServant(BaseModel) :
    id : str
    id_servant : str
    deskripsi : str
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
    vendee : UserBase

class PesananWithVendeeServant(PesananBase) :
    detail_servant : PesananServant
    detail_vendee : PesananVendee

class PesananWithVendee(PesananBase) :
    detail_vendee : PesananVendee

class OrdernWithVendeeServant(OrderBase) :
    detail_servant : PesananServant
    detail_vendee : PesananVendee
    pesanan : PesananBase