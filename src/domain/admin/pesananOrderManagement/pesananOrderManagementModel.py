from ....models.pesananModel import Status_Pesanan_Enum
from pydantic import BaseModel
from datetime import datetime as DateTimetype


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
    detail_vendee : dict

class OrderBase(BaseModel) :
    id : str
    payment_using : str
    price : int
    dateTime : DateTimetype
    detail_vendee : dict
