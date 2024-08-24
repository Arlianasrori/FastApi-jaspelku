from pydantic import BaseModel,EmailStr
from typing import Union
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from ...models_domain.servantModel import ServantBase

# pelayanan servant
class AddPelayananServantCategory(BaseModel) :
    name : str
    price : int

class UpdatePelayananServantCategory(BaseModel) :
    name : str

class ResponsePelayananServantCategory(BaseModel) :
    id : str 
    name : str
    price : int


# add
class AddDetailservant(BaseModel) : 
    deskripsi : str
    id_pelayanan : str

class AddServant(BaseModelWithPhoneValidation) :
    username : str
    email : EmailStr
    no_telepon : str
    password : str
    isVerify : bool = True
    role : RoleUser = RoleUser.servant

class AddAlamat(BaseModel) :
    village : str
    subdistrick : str
    regency : str
    province : str
    country : str
    latitude : str | None = None
    longitude : str | None = None

class AddTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : str
    isi : str

class UpdateTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : Union[str,None] = None
    isi : Union[str,None] = None

# update
class UpdateDetailservant(BaseModel) : 
    deskripsi : str | None = None
    id_pelayanan : str | None = None

class UpdateServant(BaseModelWithPhoneValidation) :
    username : str | None = None
    email : EmailStr | None = None
    no_telepon : str = None
    password : str | None = None

class UpdateAlamat(BaseModel) :
    village : str | None = None
    subdistrick : str | None = None
    regency : str | None = None
    province : str | None = None
    country : str | None = None
    latitude : str | None = None
    longitude : str | None = None

# search
class SearchServant(BaseModel) :
    username : str | None = None
    online : bool | None = None
    ready_order : bool | None = None

    model_config = {
        "json_schema": {
            "examples": [
                {
                    "username" : "habil",
                    "online": True,
                    "ready_order" : True
                }
            ]
        }
    }

class SearchServantResponse(BaseModel) :
    servant : list[ServantBase]
    count_data : int
    count_page : int