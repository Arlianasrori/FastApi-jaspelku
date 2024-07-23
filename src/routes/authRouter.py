from fastapi import APIRouter, Depends, Request, Response

from ..domain.admin.auth.authModels import LoginModel 
from ..domain.admin.auth.authService import login,refresh_token
from ..utils.sessionDepedency import sessionDepedency
from ..auth.refreshTokenAdmin import refresh_token_auth


authRouter = APIRouter(prefix="/auth")

@authRouter.post("/admin/login")
def adminLogin(data : LoginModel,res : Response,session : sessionDepedency) :
    return login(data,session,res)
@authRouter.post("/admin/refresh_token",dependencies=[Depends(refresh_token_auth)])
def adminLogin(req : Request,res : Response) :
    return refresh_token(req.refresh_admin,res)
