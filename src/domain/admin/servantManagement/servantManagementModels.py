from pydantic import BaseModel,EmailStr
from typing import Union
from ....models.userModel import RoleUser
from ....utils.BaseModelWithPhone import BaseModelWithPhoneValidation
from ...models_domain.servantModel import ServantBase

# pelayanan servant
class AddPelayananServantCategory(BaseModel) :
    name : str

class UpdatePelayananServantCategory(BaseModel) :
    name : str

class ResponsePelayananServantCategory(BaseModel) :
    id : str 
    name : str


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
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

class AddTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : str
    isi : str

class UpdateTujuanServantCategory(BaseModel) :
    id_tujuan_user_category : Union[str,None] = None
    isi : Union[str,None] = None

# update
class UpdateDetailservant(BaseModel) : 
    deskripsi : Union[str | None] = None
    id_pelayanan : Union[str | None] = None

class UpdateServant(BaseModelWithPhoneValidation) :
    username : Union[str | None] = None
    email : Union[EmailStr | None] = None
    no_telepon : str = None
    password : Union[str | None] = None

class UpdateAlamat(BaseModel) :
    village : Union[str | None] = None
    subdistrick : Union[str | None] = None
    regency : Union[str | None] = None
    province : Union[str | None] = None
    country : Union[str | None] = None
    latitude : Union[str | None] = None
    longitude : Union[str | None] = None

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