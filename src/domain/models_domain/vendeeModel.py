from pydantic import BaseModel,EmailStr
from typing import Union
from .pesananOrderModel import PesananBase,OrderBase,PesananServant
from ...utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from .userModel import AlamatBase

class PesananVendee(PesananBase) :
    detail_servant : PesananServant

class OrderVendee(OrderBase) :
    pesanan : PesananVendee

class DetailVendeeBase(BaseModel) :
    id : str
    id_vendee : str
    deskripsi : Union[str,None] = None
    saldo : int

class MoreDetailVendee(DetailVendeeBase) :
    pesanans : list[PesananVendee] = []
    orders  : list[OrderVendee] = []

class VendeeBase(BaseModelWithPhoneValidation) : 
    id : str
    username : str
    email : EmailStr
    no_telepon : str
    foto_profile : Union[str,None]
    isVerify : bool
    vendee : DetailVendeeBase 
    alamat : Union[AlamatBase,None] = None

class MoreVendee(VendeeBase) :
    vendee : MoreDetailVendee
