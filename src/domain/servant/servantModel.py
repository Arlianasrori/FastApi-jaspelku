from pydantic import BaseModel,root_validator
from ..models_domain.servantModel import MoreDetailServant,ServantBase,TimeServant,DetailServantWithoutRatingPesananOrder
from ..models_domain.userModel import AlamatBase
from ...models.servantModel import DayEnum
from python_random_strings import random_strings

class AddJadwalPelayanan(BaseModel) :
    day : DayEnum
    
class AddDetailServant(BaseModel) :
    timeServant : str
    deskripsi : str
    id_pelayanan : str
    alamat : AlamatBase
    jadwal : list[AddJadwalPelayanan]
    id_tujuan_servant_category : str | None = None
  
class ResponseAddDetailServant(ServantBase) :
    servant : DetailServantWithoutRatingPesananOrder
    