from pydantic import BaseModel,field_validator
from datetime import datetime as DateTime
from .userModel import UserBase
from ...models.notifikasiModel import NotifikasiCategory_Enum

class NotifikasiBase(BaseModel) :
    id : str
    id_user : str
    title : str
    notifikasi_category_id : NotifikasiCategory_Enum
    isi : str
    id_pesanan : str | None = None
    datetime : DateTime

class AddNotifikasiBody(BaseModel) :
    id_user : str
    notifikasi_category_id : NotifikasiCategory_Enum
    title : str
    isi : str
    id_pesanan : str | None = None

class NotifikasiWithUser(NotifikasiBase) :
    user : UserBase

class NotifikasiRead(BaseModel) :
    id : str
    id_user : str
    id_notifikasi : str
    isRead : bool

class NotifikasiwithUserRead(NotifikasiWithUser) :
    notifikasi_read : NotifikasiRead | None = None

    @field_validator("notifikasi_read",mode="before")
    def notifikasi_read_validation(cls,v) :
        if v is None or len(v) == 0 :
            return None
        return v[0]