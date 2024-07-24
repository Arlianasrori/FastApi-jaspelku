from fastapi import APIRouter, Depends, Request, Response

from ..domain.admin.auth.authModels import LoginModel,ResponseLoginAdmin
from ..domain.admin.auth.authService import login,refresh_token
from ..utils.sessionDepedency import sessionDepedency
from ..auth.refreshTokenAdmin import refresh_token_auth
from ..models.responseModel import ResponseModel


authRouter = APIRouter(prefix="/auth")

@authRouter.post("/admin/login",response_model=ResponseModel[ResponseLoginAdmin])
def adminLogin(data : LoginModel,res : Response,session : sessionDepedency) :
    return login(data,session,res)
@authRouter.post("/admin/refresh_token",dependencies=[Depends(refresh_token_auth)],response_model=ResponseModel[ResponseLoginAdmin])
def adminLogin(req : Request,res : Response) :
    return refresh_token(req.refresh_admin,res)