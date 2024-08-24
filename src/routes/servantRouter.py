from fastapi import APIRouter,Depends
from ..domain.servant.servantModel import AddDetailServant,ResponseAddUpdateDetailServant,ResponseProfilServant,ResponseGetServant,UpdateProfileServant,ResponseDetailProfileServant,ResponseRatingsServant,ResponseGetRatingById,ResponseGetPesanans,ResponseGetPesananBYId,ResponseAddUpdateLocationNow,AddUpdateLocationNowBody
from ..domain.models_domain.servantModel import ServantBase,ServantWithOutAlamat
from ..domain.servant import servantService
from ..models.pesananModel import Status_Pesanan_Enum
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..auth.dependAuthMiddleware.servantAuth import servantAuthDepends
from ..utils.sessionDepedency import sessionDepedency
from ..models.responseModel import ResponseModel
from ..error.errorHandling import SocketException

# socket
from ..socket.socket import sio
from ..socket.socketErrorHandling import socketError
from ..db.database import SessionLocal
from pydantic_core._pydantic_core import ValidationError

servantRouter = APIRouter(prefix="/servant",dependencies=[Depends(userAuthDepends),Depends(servantAuthDepends)])

# profile
@servantRouter.post("/detail_servant",response_model=ResponseModel[ResponseAddUpdateDetailServant],tags=["SERVANT/PROFILE"])
async def addDetailServant(detail_servant : AddDetailServant,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.addDetailServant(user["id"],detail_servant,session)

@servantRouter.patch("/profile",response_model=ResponseModel[ResponseAddUpdateDetailServant],tags=["SERVANT/PROFILE"])
async def updateProfile(update_servant : UpdateProfileServant,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.updateProfileServant(user["id"],update_servant,session)

@servantRouter.get("/profile",response_model=ResponseModel[ResponseProfilServant],tags=["SERVANT/PROFILE"])
async def getProfileServant(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    print("tes")
    return await servantService.getProfilServant(user["id"],session)

@servantRouter.get("/detailProfile",response_model=ResponseModel[ResponseDetailProfileServant],tags=["SERVANT/PROFILE"])
async def getProfileMoreDetail(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.getDetailProfileServant(user["id"],session)


# home
@servantRouter.get("/ratings",response_model=ResponseModel[ResponseRatingsServant],tags=["SERVANT/PROFILE"])
async def getRatingsServant(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.getRatings(user["id"],session)

@servantRouter.get("/rating/{id_rating}",response_model=ResponseModel[ResponseGetRatingById],tags=["SERVANT/PROFILE"])
async def getRatingById(id_rating : str,session : sessionDepedency = None) :
    return await servantService.getRatingById(id_rating,session)


# auth
@servantRouter.get("/getServant",response_model=ResponseModel[ResponseGetServant],tags=["SERVANT/PROFILE"])
async def getServant(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.getServant(user["id"],session)


# pesanan
@servantRouter.get("/pesanans",response_model=ResponseModel[ResponseGetPesanans],tags=["SERVANT/PESANAN"])
async def getPesanans(status_pesanan : Status_Pesanan_Enum | None = None,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.getPesanans(user["id"],status_pesanan,session)

@servantRouter.get("/pesanan/{id_pesanan}",response_model=ResponseModel[ResponseGetPesananBYId],tags=["SERVANT/PESANAN"])
async def getPesananById(id_pesanan : str | None = None,session : sessionDepedency = None) :
    return await servantService.getPesananById(id_pesanan,session)

@servantRouter.put("/pesanan/cancel/{id_pesanan}",response_model=ResponseModel[ResponseGetPesananBYId],tags=["SERVANT/PESANAN"])
async def cancelPesanan(id_pesanan : str | None = None,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.batalkanPesananServant(id_pesanan,user["id"],session)

@servantRouter.put("/pesanan/approved/{id_pesanan}",response_model=ResponseModel[ResponseGetPesananBYId],tags=["SERVANT/PESANAN"])
async def approvedPesanan(approved : bool,id_pesanan : str | None = None,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.approvedPesananServant(id_pesanan,user["id"],approved,session)


# ready order
@servantRouter.get("/readyOrder",response_model=ResponseModel[ServantWithOutAlamat],tags=["SERVANT/READYORDER"])
async def getReadyOrder(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.getReadyOrder(user["id"],session)

@servantRouter.put("/readyOrder",response_model=ResponseModel[ServantBase],tags=["SERVANT/READYORDER"])
async def updateReadyOrder(readyOrder : bool,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.updateReadyOrder(readyOrder,user["id"],session)

@servantRouter.post("/location_now",response_model=ResponseModel[ResponseAddUpdateLocationNow],tags=["SERVANT/LOCATION"])
async def addUpdateLocationNow(location_data : AddUpdateLocationNowBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.addUpdateLocationNow(user["id"],location_data,session)

# # socket
# session = SessionLocal()
# # location now
# @sio.on("share_servant_location")
# async def receive_location(sid, data):
#     try :
#         print("Msg receive from " + str(sid))
#         updateAddLocation = await servantService.addUpdateLocationNow(data["id_user"],data["location"],session)
#         await sio.emit("share_servant_location",updateAddLocation)   
#     except SocketException as err:
#         await socketError(err.status,err.messsage,err.type,sid)
#     except ValidationError as err :
#         await socketError(400,err.errors()[0]["msg"],"share_location",sid)
#     except Exception as err :
#         await socketError(500,"internal server error","server",sid)

