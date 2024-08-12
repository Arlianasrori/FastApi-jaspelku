from fastapi import APIRouter,Depends
from ..domain.servant.servantModel import AddDetailServant,ResponseAddDetailServant
from ..domain.servant import servantService
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..utils.sessionDepedency import sessionDepedency
from ..models.responseModel import ResponseModel

servantRouter = APIRouter(prefix="/servant",dependencies=[Depends(userAuthDepends)])

@servantRouter.post("/detail_servant",response_model_exclude={"orders","pesanans","rating"},response_model=ResponseModel[ResponseAddDetailServant])
async def addDetailServant(detail_servant : AddDetailServant,user : dict = Depends(GetUserDepends),session : sessionDepedency = None) :
    return await servantService.addDetailServant(user["id"],detail_servant,session)