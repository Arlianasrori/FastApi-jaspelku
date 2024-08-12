from fastapi import APIRouter

# user management
from ..domain.admin.userManagement.userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ..domain.admin.userManagement import userManagementService

from ..models.responseModel import ResponseModel

# servant management
from ..domain.admin.servantManagement.servantManagementModels import AddPelayananServantCategory,UpdatePelayananServantCategory,ResponsePelayananServantCategory,AddServant,AddDetailservant,AddAlamat,UpdateServant,UpdateDetailservant,UpdateAlamat,SearchServant,SearchServantResponse,AddTujuanServantCategory,UpdateTujuanServantCategory
from ..domain.admin.servantManagement import servantManagementService 
from ..domain.models_domain.servantModel import MoreServantBase,TujuanServantCategoryBase,ServantBase

# vendee management
from ..domain.admin.vendeeManagement.vendeeManagementModel import AddVendee,AddAlamat,AddDetailVendee,SearchVendee,SearchVendeeResponse,Updatevendee,UpdateAlamat,UpdateDetailVendee,TujuanVendeeCategoryBase,AddTujuanVendeeCategory,UpdateTujuanVendeeCategory
from ..domain.admin.vendeeManagement import vendeeManagementService
from ..domain.models_domain.vendeeModel import MoreVendee,VendeeBase

# pesanan order management
from ..domain.admin.pesananOrderManagement.pesananOrderManagementModel import SearchPesananOrder,SearchPesananResponse,SearchOrderResponse,StatisticPesanan,StatisticOrder,ResponseOverviewPesanan,ResponseOverviewOrder
from ..domain.admin.pesananOrderManagement import pesananOrderManagementService
from ..domain.models_domain.pesananOrderModel import OrdernWithVendeeServant,PesananWithVendeeServant

from ..utils.sessionDepedency import sessionDepedency
from ..auth.dependAuthMiddleware.adminAuthCookie import adminCookieAuth
from fastapi import Depends,Body
from typing import Annotated

adminRouter = APIRouter(prefix="/admin",dependencies=[Depends(adminCookieAuth)])

# tujuan user category
@adminRouter.post("/tujuan_user_category",response_model=ResponseModel[ResponseTujuanUserCategory],tags=["USER/TUJUAN_USER_CATEGORY"])
async def addTujuanUserCategory(data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    return await userManagementService.add_tujuan_user_category(data,session)

@adminRouter.put("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory],tags=["USER/TUJUAN_USER_CATEGORY"])
async def updateTujuanUserCategory(id: str,data : AddUpdateTujuanUserCategory,session : sessionDepedency) :
    print("tes lagi")
    return await userManagementService.update_tujuan_user_category(id,data,session)

@adminRouter.delete("/tujuan_user_category/{id}",response_model=ResponseModel[ResponseTujuanUserCategory],tags=["USER/TUJUAN_USER_CATEGORY"])
async def deleteTujuanUserCategory(id : str,session : sessionDepedency) :
    return await userManagementService.delete_tujuan_user_category(id,session)

@adminRouter.get("/tujuan_user_category",response_model=ResponseModel[list[ResponseTujuanUserCategory]],tags=["USER/TUJUAN_USER_CATEGORY"])
async def getTujuanUserCategory(session : sessionDepedency) :
    return await userManagementService.getAll_tujuan_user_category(session)

# SERVANT

# pelayanan servant
@adminRouter.post("/pelayanan_servant_category",response_model=ResponseModel[ResponsePelayananServantCategory],tags=["SERVANT/PELAYANAN_CATEGORY"])
async def addpelayananCategory(data : AddPelayananServantCategory,session : sessionDepedency) :
    return await servantManagementService.addPelayananServant(data,session)

@adminRouter.put("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory],tags=["SERVANT/PELAYANAN_CATEGORY"])
async def updatepelayananCategory(id : str,data : UpdatePelayananServantCategory,session : sessionDepedency) :
    return await servantManagementService.updatePelayananServantCategory(id,data,session)

@adminRouter.delete("/pelayanan_servant_category/{id}",response_model=ResponseModel[ResponsePelayananServantCategory],tags=["SERVANT/PELAYANAN_CATEGORY"])
async def deletepelayananCategory(id : str,session : sessionDepedency) :
    return await servantManagementService.deletePelayananServantCategory(id,session)

@adminRouter.get("/pelayanan_servant_category",response_model=ResponseModel[list[ResponsePelayananServantCategory]],tags=["SERVANT/PELAYANAN_CATEGORY"])
async def getAllpelayananCategory(session : sessionDepedency) :
    return await servantManagementService.getAllPelayananServantCategory(session)


# servant
@adminRouter.get("/servant",response_model=ResponseModel[list[ServantBase]],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def getAllServant(session : sessionDepedency) :
    return await servantManagementService.getAllServants(session)

@adminRouter.get("/servant/search",response_model=ResponseModel[SearchServantResponse],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def searchServant(page : int,filter : Annotated[SearchServant,Body(examples=[{"username" : "habil","online": True,"ready_order" : True}])] = SearchServant(),session : sessionDepedency = None) :
    return await servantManagementService.searchServant(page,filter,session)

@adminRouter.get("/servant/{id}",response_model=ResponseModel[MoreServantBase],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def getServantById(id : str,session : sessionDepedency) :
    return await servantManagementService.getServantById(id,session)

@adminRouter.post("/servant",response_model=ResponseModel[ServantBase],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def addServant(servant : AddServant,alamat : AddAlamat,detail_servant : AddDetailservant,session : sessionDepedency) :
    return await servantManagementService.add_servant(servant,alamat,detail_servant,session)

@adminRouter.put("/servant/{id}",response_model=ResponseModel[ServantBase],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def updateServant(id : str,servant : UpdateServant | None = None,alamat : UpdateAlamat| None = None,detail_servant : UpdateDetailservant | None = None,session : sessionDepedency = None) :
    return await servantManagementService.update_servant(id,servant,alamat,detail_servant,session)

@adminRouter.delete("/servant/{id}",response_model=ResponseModel[ServantBase],tags=["SERVANT/SERVANT_MANAGEMENT"])
async def deleteServant(id : str,session : sessionDepedency) :
    return await servantManagementService.delete_servant(id,session)



# vendee
@adminRouter.get("/vendee",response_model=ResponseModel[list[VendeeBase]],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def getAllVendee(session : sessionDepedency) :
    return await vendeeManagementService.getAllvendees(session)

@adminRouter.get("/vendee/search",response_model=ResponseModel[SearchVendeeResponse],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def searchVendee(page : int,filter : Annotated[SearchVendee,Body(examples=[{"username" : "habil","online" : True}])] = SearchVendee(),session : sessionDepedency = None) :
    return await vendeeManagementService.searchvendee(page,filter,session)

@adminRouter.get("/vendee/{id}",response_model=ResponseModel[MoreVendee],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def getVendeeById(id : str,session : sessionDepedency) :
    return await vendeeManagementService.getvendeeById(id,session)

@adminRouter.post("/vendee",response_model=ResponseModel[VendeeBase],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def addVendee(vendee : AddVendee,alamat : AddAlamat,detail_vendee : AddDetailVendee,session : sessionDepedency) :
    return await vendeeManagementService.add_vendee(vendee,alamat,detail_vendee,session)

@adminRouter.put("/vendee/{id}",response_model=ResponseModel[VendeeBase],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def updatevendee(id : str,vendee : Updatevendee | None = None,alamat : UpdateAlamat| None = None,detail_vendee : UpdateDetailVendee | None = None,session : sessionDepedency = None) :
    return await vendeeManagementService.update_vendee(id,vendee,alamat,detail_vendee,session)

@adminRouter.delete("/vendee/{id}",response_model=ResponseModel[VendeeBase],tags=["VENDEE/VENDEE_MANAGEMENT"])
async def deletevendee(id : str,session : sessionDepedency) :
    return await vendeeManagementService.delete_vendee(id,session)


# tujuan servant category
@adminRouter.get("/tujuan_servant_category",response_model=ResponseModel[list[TujuanServantCategoryBase]],tags=["SERVANT/TUJUAN_SERVANT_CATEGORY"])
async def getAllTujuanServantCategory(session : sessionDepedency) :
    return await servantManagementService.getAllTujuanServantCategory(session)

@adminRouter.get("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase],tags=["SERVANT/TUJUAN_SERVANT_CATEGORY"])
async def getTujuanServantCategoryById(id : str,session : sessionDepedency) :
    return await servantManagementService.getTujuanServantCategoryById(id,session)

@adminRouter.post("/tujuan_servant_category",response_model=ResponseModel[TujuanServantCategoryBase],tags=["SERVANT/TUJUAN_SERVANT_CATEGORY"])
async def addTujuanServantCategoryById(tujuan_servant_category : AddTujuanServantCategory,session : sessionDepedency) :
    return await servantManagementService.addTujuanServantCategory(tujuan_servant_category,session)

@adminRouter.put("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase],tags=["SERVANT/TUJUAN_SERVANT_CATEGORY"])
async def updateTujuanServantCategory(id : str,tujuan_servant_category : UpdateTujuanServantCategory | None = None,session : sessionDepedency = None) :
    return await servantManagementService.updateTujuanServantCategory(id,tujuan_servant_category,session)

@adminRouter.delete("/tujuan_servant_category/{id}",response_model=ResponseModel[TujuanServantCategoryBase],tags=["SERVANT/TUJUAN_SERVANT_CATEGORY"])
async def deleteTujuanServantCategory(id : str,session : sessionDepedency) :
    return await servantManagementService.deleteTujuanServantCategory(id,session)


# tujuan vendee category
@adminRouter.get("/tujuan_vendee_category",response_model=ResponseModel[list[TujuanVendeeCategoryBase]],tags=["VENDEE/TUJUAN_VENDEE_CATEGORY"])
async def getAllTujuanVendeeCategory(session : sessionDepedency) :
    return await vendeeManagementService.getAllTujuanVendeeCategory(session)

@adminRouter.get("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase],tags=["VENDEE/TUJUAN_VENDEE_CATEGORY"])
async def getTujuanVendeeCategoryById(id : str,session : sessionDepedency) :
    return await vendeeManagementService.getTujuanVendeeCategoryById(id,session)

@adminRouter.post("/tujuan_vendee_category",response_model=ResponseModel[TujuanVendeeCategoryBase],tags=["VENDEE/TUJUAN_VENDEE_CATEGORY"])
async def addTujuanVendeeCategoryById(tujuan_vendee_category : AddTujuanVendeeCategory,session : sessionDepedency) :
    return await vendeeManagementService.addTujuanVendeeCategory(tujuan_vendee_category,session)

@adminRouter.put("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase],tags=["VENDEE/TUJUAN_VENDEE_CATEGORY"])
async def updateTujuanVendeeCategory(id : str,tujuan_vendee_category : UpdateTujuanVendeeCategory | None = None,session : sessionDepedency = None) :
    return await vendeeManagementService.updateTujuanVendeeCategory(id,tujuan_vendee_category,session)

@adminRouter.delete("/tujuan_vendee_category/{id}",response_model=ResponseModel[TujuanVendeeCategoryBase],tags=["VENDEE/TUJUAN_VENDEE_CATEGORY"])
async def deleteTujuanVendeeCategory(id : str,session : sessionDepedency) :
    return await vendeeManagementService.deleteTujuanvendeeCategory(id,session)


# pesanan 
@adminRouter.get("/pesanan/search",response_model=ResponseModel[SearchPesananResponse],tags=["PESANAN"])
async def searchPesanan(page : int,filter : Annotated[SearchPesananOrder,Body(examples=[{"servant" : "878654","vendee" : "985775","tugas" : "menitip barang","year" : 2024,"month" : 8,"day" : 16}])] = SearchPesananOrder(),session : sessionDepedency = None) :
    return await pesananOrderManagementService.searchPesanan(page,filter,session)

@adminRouter.get("/pesanan/analitic/search",response_model=ResponseModel[StatisticPesanan],tags=["PESANAN"])
async def searchAnaliticPesanan(filter : Annotated[SearchPesananOrder,Body(examples=[{"servant" : "878654","vendee" : "985775","tugas" : "menitip barang","year" : 2024,"month" : 8,"day" : 16}])] = SearchPesananOrder(),session : sessionDepedency = None) :
    return await pesananOrderManagementService.searchStatisticPesanan(filter,session)

@adminRouter.get("/pesanan/statistic/today",response_model=ResponseModel[StatisticPesanan],tags=["PESANAN"])
async def getStatisticPesananToday(session : sessionDepedency = None) :
    return await pesananOrderManagementService.getStatisticPesananToday(session)

@adminRouter.get("/pesanan/{id}",response_model=ResponseModel[PesananWithVendeeServant],tags=["PESANAN"])
async def getPesananById(id : str,session : sessionDepedency = None) :
    return await pesananOrderManagementService.getPesananById(id,session)

@adminRouter.get("/pesanan/overview/{year}",response_model=ResponseModel[ResponseOverviewPesanan],tags=["PESANAN"])
async def getPesananById(year : int,session : sessionDepedency = None) :
    return await pesananOrderManagementService.getOverviewPesananByYear(year,session)


# order
@adminRouter.get("/order/search",response_model=ResponseModel[SearchOrderResponse],tags=["ORDER"])
async def searchOrder(page : int,filter : Annotated[SearchPesananOrder,Body(examples=[{"servant" : "878654","vendee" : "985775","tugas" : "menitip barang","year" : 2024,"month" : 8,"day" : 16}])] = SearchPesananOrder(),session : sessionDepedency = None) :
    return await pesananOrderManagementService.searchOrder(page,filter,session)

@adminRouter.get("/order/statistic/search",response_model=ResponseModel[StatisticOrder],tags=["ORDER"])
async def searchStatisticOrder(filter : Annotated[SearchPesananOrder,Body(examples=[{"servant" : "878654","vendee" : "985775","tugas" : "menitip barang","year" : 2024,"month" : 8,"day" : 16}])] = SearchPesananOrder(),session : sessionDepedency = None) :
    return await pesananOrderManagementService.searchstatisticOrder(filter,session)

@adminRouter.get("/order/{id}",response_model=ResponseModel[OrdernWithVendeeServant],tags=["ORDER"])
async def getOrderById(id : str,session : sessionDepedency = None) :
    return await pesananOrderManagementService.getOrderById(id,session)

@adminRouter.get("/order/statistic/today",response_model=ResponseModel[StatisticOrder],tags=["ORDER"])
async def getStatisticOrdertoday(session : sessionDepedency = None) :
    return await pesananOrderManagementService.getOrderToday(session)

@adminRouter.get("/order/overview/{year}",response_model=ResponseModel[ResponseOverviewOrder],tags=["ORDER"])
async def getOverviewOrderByYear(year : int,session : sessionDepedency = None) :
    return await pesananOrderManagementService.getOverviewOrderByYear(year,session)
