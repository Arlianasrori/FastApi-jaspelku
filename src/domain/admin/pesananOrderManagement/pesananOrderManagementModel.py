from ....models.pesananModel import Status_Pesanan_Enum
from pydantic import BaseModel
from datetime import datetime as DateTimetype
from typing import Union


class PesananBase(BaseModel) :
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

class OrderBase(BaseModel) :
    id : str
    payment_using : str
    price : int
    dateTime : DateTimetype

class PesananWithVendeeServant(PesananBase) :
    detail_servant : dict
    detail_vendee : dict

class OrdernWithVendeeServant(PesananBase) :
    detail_servant : dict
    detail_vendee : dict
    pesanan : PesananBase

class SearchPesanan(BaseModel) :
    servant : Union[str | None] = None
    vendee : Union[str | None] = None
    tugas : Union[str | None] = None
    year : Union[int | None] = None
    month : Union[int | None] = None
    day : Union[int | None] = None
