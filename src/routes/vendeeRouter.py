from fastapi import APIRouter,Depends
from pydantic_core._pydantic_core import ValidationError
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..auth.dependAuthMiddleware.vendeeAuth import vendeeAuthDepends
from ..utils.sessionDepedency import sessionDepedency
from ..models.responseModel import ResponseModel
from ..models.pesananModel import Status_Pesanan_Enum
from ..error.errorHandling import SocketException
from ..db.database import SessionLocal

from ..domain.models_domain.vendeeModel import VendeeBase

from ..domain.vendee.vendeeModel import AddDetailVendeeBody, AddUpdateLocationNowBody, ResponseAddUpdateLocationNow,UpdateDetailVendeeBody,ResponseAddUpdateDetailVendee,SearchServantQuery,ResponseFilterServant,ResponseDetailProfileServant,ResponseRatingsServant,ResponseGetRatingById,ResponseGetPesanans,ResponseGetPesananBYId,ResponseAddUpdatePesanan,AddPesananBody,AddRatingBody,UpdateRatingBody,ResponseAddUpdateRating
from ..domain.vendee import vendeeService


# socket
from ..socket.socket import sio,online_users
from ..socket.socket_auth_middleware import auth_middleware
from ..socket.socketErrorHandling import socketError

vendeeRouter = APIRouter(prefix="/vendee",dependencies=[Depends(userAuthDepends),Depends(vendeeAuthDepends)])

@vendeeRouter.post("/detail_vendee",response_model=ResponseModel[ResponseAddUpdateDetailVendee],tags=["VENDEE/PROFILE"])
async def addDetailVendeen(detail_vendee : AddDetailVendeeBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.AddDetailVendee(user["id"],detail_vendee,session)

@vendeeRouter.get("/profile",response_model=ResponseModel[VendeeBase],tags=["VENDEE/PROFILE"])
async def getProfilevendee(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.getProfileVendee(user["id"],session)

@vendeeRouter.patch("/profile",response_model=ResponseModel[ResponseAddUpdateDetailVendee],tags=["VENDEE/PROFILE"])
async def getProfilevendee(detail_vendee : UpdateDetailVendeeBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.updateProfileVendee(user["id"],detail_vendee,session)

@vendeeRouter.get("/getVendee",response_model=ResponseModel[VendeeBase],tags=["VENDEE/AUTH"])
async def getVendee(user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.getVendee(user["id"],session)


# get servant
@vendeeRouter.get("/searchServant",response_model=ResponseModel[list[ResponseFilterServant]],tags=["VENDEE/GETSERVANT"])
async def getServantFilter(page : int,search : SearchServantQuery = SearchServantQuery(),session : sessionDepedency = None) :
    return await vendeeService.getServantFilter(page,search,session)
@vendeeRouter.get("/getServantByRating",response_model=ResponseModel[list[ResponseFilterServant]],tags=["VENDEE/GETSERVANT"])
async def getServantByRating(page : int,session : sessionDepedency = None) :
    return await vendeeService.getServantByRating(page,session)

@vendeeRouter.get("/getServant/{id_servant}",response_model=ResponseModel[ResponseDetailProfileServant],tags=["VENDEE/GETSERVANT"])
async def getServantById(id_servant : str,session : sessionDepedency = None) :
    return await vendeeService.getServantById(id_servant,session)

@vendeeRouter.get("/getServant/ratings/{id_servant}",response_model=ResponseModel[ResponseRatingsServant],tags=["VENDEE/GETSERVANT"])
async def getRatingsServant(id_servant : str,session : sessionDepedency = None) :
    return await vendeeService.getRatingServant(id_servant,session)

@vendeeRouter.get("/getServant/rating/{id_rating}",response_model=ResponseModel[ResponseGetRatingById],tags=["VENDEE/GETSERVANT"])
async def getRatingById(id_rating : str,session : sessionDepedency = None) :
    return await vendeeService.getRatingById(id_rating,session)


# pesanan
@vendeeRouter.get("/pesanans",response_model=ResponseModel[ResponseGetPesanans],tags=["VENDEE/PESANAN"])
async def getPesanans(status_pesanan : Status_Pesanan_Enum| None = None,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.getPesanans(user["id"],status_pesanan,session)

@vendeeRouter.get("/pesanan/{id_pesanan}",response_model=ResponseModel[ResponseGetPesananBYId],tags=["VENDEE/PESANAN"])
async def getPesananById(id_pesanan : str,session : sessionDepedency = None) :
    return await vendeeService.getPesananById(id_pesanan,session)

@vendeeRouter.post("/pesanan/cancel/{id_pesanan}",response_model=ResponseModel[ResponseGetPesananBYId],tags=["VENDEE/PESANAN"])
async def cancelPesanan(id_pesanan : str,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.batalkanPesanan(id_pesanan,user["id"],session)

@vendeeRouter.post("/pesanan",response_model=ResponseModel[ResponseAddUpdatePesanan],tags=["VENDEE/PESANAN"])
async def addPesanan(pesanan : AddPesananBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.AddPesanan(user["id"],pesanan,session)


# rating
@vendeeRouter.post("/rating",response_model=ResponseModel[ResponseAddUpdateRating],tags=["VENDEE/RATING"])
async def addPesanan(rating : AddRatingBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.addRating(user["id"],rating,session)

@vendeeRouter.patch("/rating/{id_rating}",response_model=ResponseModel[ResponseAddUpdateRating],tags=["VENDEE/RATING"])
async def addPesanan(id_rating : str,rating : UpdateRatingBody,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await vendeeService.updateRating(user["id"],id_rating,rating,session)

# location now
@sio.on("share_vendee_location") 
async def share_vendee_location(sid,data) :
    try :
        # check data 
        if type(data) != dict :
            raise SocketException(400,"data required or object type","location now")
        
        session = SessionLocal()
        auth = await auth_middleware(data.get("auth"))
   
        if not auth :
            raise SocketException(401,"Unauthorized","Unauthorized")
        print("Msg receive from " + str(sid))

        
        # validation location data
        locationData = data.get("location")
        if not locationData :
            raise SocketException(400,"location required","location now")
        
        locationAfterValidation = AddUpdateLocationNowBody(**locationData)
        print(locationAfterValidation)
        updateAddLocation = await vendeeService.addUpdateLocationNow(auth["id_user"],locationAfterValidation,session)
        # send data to client
        await sio.emit("share_vendee_location",updateAddLocation)   
    
    # handle error
    except SocketException as err:
        await socketError(err.status,err.messsage,err.type,sid)
    except ValidationError as err :
        await socketError(400,err.errors()[0]["msg"],"share_location",sid)
    except Exception as err :
        print(err)
        await socketError(500,"internal server error","server",sid)
    finally :
        await session.close()


