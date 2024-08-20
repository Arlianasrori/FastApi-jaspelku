from pydantic import BaseModel, Field
from ..models_domain.pesananOrderModel import PesananBase,PesananWithServant,PesananWithVendee
from ..models_domain.userModel import AlamatBase,UpdateAlamat
from ..models_domain.vendeeModel import VendeeBase,DetailVendeeBase,TujuanVendeeBase,DetailVendeetWihtVendee
from ..models_domain.servantModel import ServantBase,ServantWithOutDetail,DetailServantBase,JadwalPelayananServant,TimeServant,DetailServantWithRating,RatingServant,DetailServantWihtServant

# add detail vendee
class add_tujuan_vendee(BaseModel) :
    id_tujuan_vendee_category : str

class AddDetailVendeeBody(BaseModel) :
    deskripsi : str
    work : str
    id_tujuan_vendee_categories : list[add_tujuan_vendee]
    alamat : AlamatBase

class UpdateDetailVendeeBody(BaseModel) :
    deskripsi : str | None = None
    work : str | None = None
    alamat : UpdateAlamat | None = None

class DetailVendeeWithtujuan(DetailVendeeBase) :
    tujuan_vendee : list[TujuanVendeeBase]
    
class ResponseAddUpdateDetailVendee(VendeeBase) :
    vendee : DetailVendeeWithtujuan




# get servant 
class SearchServantQuery(BaseModel) :
    username : str | None = None
    id_pelayanan : str | None = None

class DetailServantResponseFilter(DetailServantBase) :
    jadwal_pelayanan : list[JadwalPelayananServant] = []
    time_servant : TimeServant | None = None 
    rating : int

class ResponseFilterServant(ServantWithOutDetail) :
    servant : DetailServantResponseFilter


class StatistikPenjualan(BaseModel) :
    total_pesanan : int
    pengajuan : int 
    proses : int
    dibatalkan : int
    membatalkan : int
    selesai : int

class DetailProfileServant(DetailServantBase) :
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
class DetailVendeeWithPesanan(DetailVendeeBase) :
    pesanans : list[PesananWithServant] 

class DetailVendeeWithPesananDict(DetailVendeeBase) :
    pesanan : PesananWithServant 

class ResponseGetPesanans(BaseModel) :
    id : str
    username : str
    email : str
    vendee : DetailVendeeWithPesanan

class ResponseGetPesananBYId(BaseModel) :
    id : str
    username : str
    email : str
    vendee : DetailVendeeWithPesananDict

# add pesanan
class AddPesananBody(BaseModel) :
    id_user_servant : str
    additional_information : str
    order_estimate :  str

class ResponseAddUpdatePesanan(PesananBase) :
    detail_vendee : DetailVendeetWihtVendee
    detail_servant : DetailServantWihtServant

# rating
class AddRatingBody(BaseModel) :
    id_user_servant : str
    rating : int = Field(gt=0,le=5)
    isi : str
class UpdateRatingBody(BaseModel) :
    rating : int | None = None
    isi : str | None = None

class ResponseAddUpdateRating(BaseModel) :
    id : str
    id_detail_servant : str
    id_detail_vendee : str
    rating : int = Field(gt=0,le=5)
    isi : str