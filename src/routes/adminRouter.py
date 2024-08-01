from fastapi import APIRouter

# user management
from ..domain.admin.userManagement.userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ..domain.admin.userManagement import userManagementService

from ..models.responseModel import ResponseModel

# servant management
from ..domain.admin.servantManagement.servantManagementModels import AddPelayananServantCategory, ServantBase,UpdatePelayananServantCategory,ResponsePelayananServantCategory,AddServant,AddDetailservant,AddAlamat,UpdateServant,UpdateDetailservant,UpdateAlamat,SearchServant,SearchServantResponse,MoreServantBase,AddTujuanServantCategory,UpdateTujuanServantCategory,TujuanServantCategoryBase
from ..domain.admin.servantManagement import servantManagementService 

# vendee management
from ..domain.admin.vendeeManagement.vendeeManagementModel import VendeeBase,MoreVendee,AddVendee,AddAlamat,AddDetailVendee,SearchVendee,SearchVendeeResponse,Updatevendee,UpdateAlamat,UpdateDetailVendee,TujuanVendeeCategoryBase,AddTujuanVendeeCategory,UpdateTujuanVendeeCategory
from ..domain.admin.vendeeManagement import vendeeManagementService

# pesanan order management
from ..domain.admin.pesananOrderManagement.pesananOrderManagementModel import SearchPesanan,PesananBase,OrderBase,OrdernWithVendeeServant,PesananWithVendeeServant
from ..domain.admin.pesananOrderManagement import pesananOrderManagementService


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
    return await servantManagementService.getAllServants(session)

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
async def deleteServant(id : str,session : sessionDepedency) :
    return await servantManagementService.delete_servant(id,session)



# vendee
@adminRouter.get("/vendee",response_model=ResponseModel[list[VendeeBase]])
async def getAllVendee(session : sessionDepedency) :
    return await vendeeManagementService.getAllvendees(session)

@adminRouter.get("/vendee/search",response_model=ResponseModel[SearchVendeeResponse])
async def searchVendee(page : int,filter : SearchVendee | None = SearchVendee(),session : sessionDepedency = None) :
    return await vendeeManagementService.searchvendee(page,filter,session)

@adminRouter.get("/vendee/{id}",response_model=ResponseModel[MoreVendee])
async def getVendeeById(id : str,session : sessionDepedency) :
    return await vendeeManagementService.getvendeeById(id,session)

@adminRouter.post("/vendee",response_model=ResponseModel[VendeeBase])
async def addVendee(vendee : AddVendee,alamat : AddAlamat,detail_vendee : AddDetailVendee,session : sessionDepedency) :
    return await vendeeManagementService.add_vendee(vendee,alamat,detail_vendee,session)

@adminRouter.put("/vendee/{id}",response_model=ResponseModel[VendeeBase])
async def updatevendee(id : str,vendee : Updatevendee | None = None,alamat : UpdateAlamat| None = None,detail_vendee : UpdateDetailVendee | None = None,session : sessionDepedency = None) :
    return await vendeeManagementService.update_vendee(id,vendee,alamat,detail_vendee,session)

@adminRouter.delete("/vendee/{id}",response_model=ResponseModel[VendeeBase])
async def deletevendee(id : str,session : sessionDepedency) :
    return await vendeeManagementService.delete_vendee(id,session)


# tujuan servant category
@adminRouter.get("/tujuan_servant_category",response_model=ResponseModel[list[TujuanServantCategoryBase]])
async def getAllTujuanServantCategory(session : sessionDepedency) :
    return await servantManagementService.getAllTujuanServantCategory(session)

@adminRouter.get("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase])
async def getTujuanServantCategoryById(id : str,session : sessionDepedency) :
    return await servantManagementService.getTujuanServantCategoryById(id,session)

@adminRouter.post("/tujuan_servant_category",response_model=ResponseModel[TujuanServantCategoryBase])
async def addTujuanServantCategoryById(tujuan_servant_category : AddTujuanServantCategory,session : sessionDepedency) :
    return await servantManagementService.addTujuanServantCategory(tujuan_servant_category,session)

@adminRouter.put("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase])
async def updateTujuanServantCategory(id : str,tujuan_servant_category : UpdateTujuanServantCategory | None = None,session : sessionDepedency = None) :
    return await servantManagementService.updateTujuanServantCategory(id,tujuan_servant_category,session)

@adminRouter.delete("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase])
async def deleteTujuanServantCategory(id : str,session : sessionDepedency) :
    return await servantManagementService.deleteTujuanServantCategory(id,session)


# tujuan servant category
@adminRouter.get("/tujuan_vendee_category",response_model=ResponseModel[list[TujuanVendeeCategoryBase]])
async def getAllTujuanVendeeCategory(session : sessionDepedency) :
    return await vendeeManagementService.getAllTujuanVendeeCategory(session)

@adminRouter.get("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase])
async def getTujuanVendeeCategoryById(id : str,session : sessionDepedency) :
    return await vendeeManagementService.getTujuanVendeeCategoryById(id,session)

@adminRouter.post("/tujuan_vendee_category",response_model=ResponseModel[TujuanVendeeCategoryBase])
async def addTujuanVendeeCategoryById(tujuan_vendee_category : AddTujuanServantCategory,session : sessionDepedency) :
    return await vendeeManagementService.addTujuanVendeeCategory(tujuan_vendee_category,session)

@adminRouter.put("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase])
async def updateTujuanVendeeCategory(id : str,tujuan_vendee_category : UpdateTujuanServantCategory | None = None,session : sessionDepedency = None) :
    return await vendeeManagementService.updateTujuanVendeeCategory(id,tujuan_vendee_category,session)

@adminRouter.delete("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase])
async def deleteTujuanVendeeCategory(id : str,session : sessionDepedency) :
    return await vendeeManagementService.deleteTujuanvendeeCategory(id,session)


# pesanan 
@adminRouter.get("/pesanan/search")
async def searchPesanan(page : int,filter : SearchPesanan,session : sessionDepedency) :
    return await pesananOrderManagementService.searchPesanan(page,filter,session)