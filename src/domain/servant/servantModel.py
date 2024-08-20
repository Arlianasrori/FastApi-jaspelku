from pydantic import BaseModel
from ..models_domain.servantModel import ServantBase,DetailServantWithoutRatingPesananOrder,DetailServantBase,TujuanServant,JadwalPelayananServant,TimeServant,DetailServantWihtServant,DetailServantWithRating,RatingServant
from ..models_domain.vendeeModel import DetailVendeetWihtVendee
from ..models_domain.pesananOrderModel import PesananBase,PesananWithVendee
from ..models_domain.userModel import AlamatBase,UpdateAlamat
from ...models.servantModel import DayEnum
from ...models.servantModel import DayEnum
from enum import Enum

class AddJadwalPelayanan(BaseModel) :
    day : DayEnum
    
class AddDetailServant(BaseModel) :
    timeServant : str
    deskripsi : str
    id_pelayanan : str
    alamat : AlamatBase
    jadwal : list[AddJadwalPelayanan]
    id_tujuan_servant_category : str | None = None
  
class ResponseAddUpdateDetailServant(ServantBase) :
    servant : DetailServantWithoutRatingPesananOrder

class ResponseProfilServant(ServantBase) :
    servant : DetailServantWithoutRatingPesananOrder

class ResponseGetServant(ServantBase) :
    servant : DetailServantBase

# update profile
class UpdateJadwalServant(BaseModel) :
    day : DayEnum
    isDelete : bool

class UpdateProfileServant(BaseModel) :
    timeServant : str | None = None
    deskripsi : str | None = None
    id_pelayanan : str | None = None
    alamat : UpdateAlamat | None = None
    jadwal : list[UpdateJadwalServant] | None = None

class StatistikPenjualan(BaseModel) :
    total_pesanan : int
    pengajuan : int 
    proses : int
    dibatalkan : int
    membatalkan : int
    selesai : int

class DetailProfileServant(DetailServantBase) :
    tujuan_servant : TujuanServant | None = None
    jadwal_pelayanan : list[JadwalPelayananServant] = []
    time_servant : TimeServant | None = None 
    rating : int
    statistik_penjualan : StatistikPenjualan
    
class ResponseDetailProfileServant(ServantBase) :
    servant : DetailProfileServant

class ResponseRatingsServant(ServantBase) :
    servant : DetailServantWithRating

class ResponseGetRatingById(RatingServant) :
    id : str
    rating : int
    isi : str
    detail_vendee : DetailVendeetWihtVendee
    detail_servant : DetailServantWihtServant


# pesanan
class DetailServantWithPesanan(DetailServantBase) :
    pesanans : list[PesananWithVendee] 

class DetailServantWithPesananDict(DetailServantBase) :
    pesanan : PesananWithVendee 

class ResponseGetPesanans(BaseModel) :
    id : str
    username : str
    email : str
    servant : DetailServantWithPesanan

class ResponseGetPesananBYId(BaseModel) :
    id : str
    username : str
    email : str
    servant : DetailServantWithPesananDict


# location now 
class AddUpdateLocationNowBody(BaseModel) :
    latitude : str
    longitude : str

class ResponseAddUpdateLocationNow(BaseModel) :
    id_user : str
    latitude : str
    longitude : str