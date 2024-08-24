from pydantic import BaseModel,field_validator
from ...models_domain.pesananOrderModel import PesananWithVendeeServant,OrdernWithVendeeServant

class SearchPesananOrder(BaseModel) :
    servant : str | None = None
    vendee : str | None = None
    tugas : str | None = None
    year : int | None = None
    month : int | None = None
    day : int | None = None

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

    @field_validator("pesanans",mode="before")
    def validate_no_telepon(cls, v) :
        print(v)
        
        return v
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