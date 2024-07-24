from fastapi import APIRouter

from ..domain.admin.userManagement.userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ..domain.admin.servantManagement.servantManagementModels import AddPelayananServantCategory,UpdatePelayananServantCategory,ResponsePelayananServantCategory
from ..models.responseModel import ResponseModel

from ..domain.admin.userManagement import userManagementService
from ..domain.admin.servantManagement import servantManagementService 

from ..utils.sessionDepedency import sessionDepedency
from ..auth.adminAuthCookie import adminCookieAuth
from fastapi import Depends

adminRouter = APIRouter(prefix="/admin",dependencies=[Depends(adminCookieAuth)])

# tujuan user category
@adminRouter.post("/tujuan_user_category",response_model=ResponseModel[ResponseTujuanUserCategory])
def addTujuanUserCategory(data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    return userManagementService.add_tujuan_user_category(data,session)

@adminRouter.put("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory])
def updateTujuanUserCategory(id: str,data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    return userManagementService.update_tujuan_user_category(id,data,session)

@adminRouter.delete("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory])
def addTujuanUserCategory(id : str,session : sessionDepedency) :
    return userManagementService.delete_tujuan_user_category(id,session)

@adminRouter.get("/tujuan_user_category",response_model=ResponseModel[list[ResponseTujuanUserCategory]])
def addTujuanUserCategory(session : sessionDepedency) :
    return userManagementService.getAll_tujuan_user_category(session)

# SERVANT

# pelayanan servant
@adminRouter.post("/pelayanan_servant_category",response_model=ResponseModel[ResponsePelayananServantCategory])
def addTujuanUserCategory(data : AddPelayananServantCategory,session : sessionDepedency) :
    return servantManagementService.addPelayananServant(data,session)

@adminRouter.put("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory])
def addTujuanUserCategory(id : str,data : AddPelayananServantCategory,session : sessionDepedency) :
    return servantManagementService.updatePelayananServantCategory(id,data,session)

@adminRouter.delete("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory])
def addTujuanUserCategory(id : str,session : sessionDepedency) :
    return servantManagementService.deletePelayananServantCategory(id,session)

@adminRouter.get("/pelayanan_servant_category",response_model=ResponseModel[list[ResponsePelayananServantCategory]])
def addTujuanUserCategory(session : sessionDepedency) :
    return servantManagementService.getAllPelayananServantCategory(session)
