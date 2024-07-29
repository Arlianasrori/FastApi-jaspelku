from fastapi import APIRouter

from ..domain.admin.userManagement.userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ..domain.admin.servantManagement.servantManagementModels import AddPelayananServantCategory, ServantBase,UpdatePelayananServantCategory,ResponsePelayananServantCategory,AddServant,AddDetailservant,AddAlamat,UpdateServant,UpdateDetailservant,UpdateAlamat,SearchServant,SearchServantResponse,MoreServantBase
from ..models.responseModel import ResponseModel

from ..domain.admin.userManagement import userManagementService
from ..domain.admin.servantManagement import servantManagementService 

from ..utils.sessionDepedency import sessionDepedency
from ..auth.adminAuthCookie import adminCookieAuth
from fastapi import Depends

adminRouter = APIRouter(prefix="/admin",dependencies=[Depends(adminCookieAuth)])

# tujuan user category
@adminRouter.post("/tujuan_user_category",response_model=ResponseModel[ResponseTujuanUserCategory])
async def addTujuanUserCategory(data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    return await userManagementService.add_tujuan_user_category(data,session)

@adminRouter.put("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory])
async def updateTujuanUserCategory(id: str,data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    print("tes lagi")
    return await userManagementService.update_tujuan_user_category(id,data,session)

@adminRouter.delete("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory])
async def addTujuanUserCategory(id : str,session : sessionDepedency) :
    return await userManagementService.delete_tujuan_user_category(id,session)

@adminRouter.get("/tujuan_user_category",response_model=ResponseModel[list[ResponseTujuanUserCategory]])
async def addTujuanUserCategory(session : sessionDepedency) :
    return await userManagementService.getAll_tujuan_user_category(session)

# SERVANT

# pelayanan servant
@adminRouter.post("/pelayanan_servant_category",response_model=ResponseModel[ResponsePelayananServantCategory])
async def addpelayananCategory(data : AddPelayananServantCategory,session : sessionDepedency) :
    return await servantManagementService.addPelayananServant(data,session)

@adminRouter.put("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory])
async def updatepelayananCategory(id : str,data : UpdatePelayananServantCategory,session : sessionDepedency) :
    return await servantManagementService.updatePelayananServantCategory(id,data,session)

@adminRouter.delete("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory])
async def deletepelayananCategory(id : str,session : sessionDepedency) :
    return await servantManagementService.deletePelayananServantCategory(id,session)

@adminRouter.get("/pelayanan_servant_category",response_model=ResponseModel[list[ResponsePelayananServantCategory]])
async def getAllpelayananCategory(session : sessionDepedency) :
    return await servantManagementService.getAllPelayananServantCategory(session)


# servant
@adminRouter.get("/servant",response_model=ResponseModel[list[ServantBase]])
async def getAllServant(session : sessionDepedency) :
    return await servantManagementService.getAllServant(session)

@adminRouter.get("/servant/search",response_model=ResponseModel[SearchServantResponse])
async def searchServant(page : int,filter : SearchServant | None = SearchServant(),session : sessionDepedency = None) :
    return await servantManagementService.searchServant(page,filter,session)

@adminRouter.get("/servant/{id}",response_model=ResponseModel[MoreServantBase])
async def getServantById(id : str,session : sessionDepedency) :
    return await servantManagementService.getServantById(id,session)

@adminRouter.post("/servant",response_model=ResponseModel[ServantBase])
async def addServant(servant : AddServant,alamat : AddAlamat,detail_servant : AddDetailservant,session : sessionDepedency) :
    return await servantManagementService.add_servant(servant,alamat,detail_servant,session)

@adminRouter.put("/servant/{id}",response_model=ResponseModel[ServantBase])
async def updateServant(id : str,servant : UpdateServant | None = None,alamat : UpdateAlamat| None = None,detail_servant : UpdateDetailservant | None = None,session : sessionDepedency = None) :
    return await servantManagementService.update_servant(id,servant,alamat,detail_servant,session)

@adminRouter.delete("/servant/{id}",response_model=ResponseModel[ServantBase])
async def updateServant(id : str,session : sessionDepedency) :
    return await servantManagementService.delete_servant(id,session)