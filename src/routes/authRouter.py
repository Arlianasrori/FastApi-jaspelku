from fastapi import APIRouter, Depends, Request, Response

from ..domain.admin.auth.authModels import LoginModel,ResponseLoginAdmin
from ..domain.admin.auth.authService import login,refresh_token
from ..utils.sessionDepedency import sessionDepedency
from ..auth.refreshTokenAdmin import refresh_token_auth
from ..models.responseModel import ResponseModel

from ..domain.auth import authService
from ..domain.auth.authModel import RegisterBody,RegisterResponse,LoginBody,LoginResponse

authRouter = APIRouter(prefix="/auth")
# admin
@authRouter.post("/admin/login",response_model=ResponseModel[ResponseLoginAdmin],tags=["AUTH/ADMIN"])
async def adminLogin(data : LoginModel,res : Response,session : sessionDepedency) :
    return await login(data,session,res)
@authRouter.post("/admin/refresh_token",dependencies=[Depends(refresh_token_auth)],response_model=ResponseModel[ResponseLoginAdmin],tags=["AUTH/ADMIN"])
def adminLogin(req : Request,res : Response) :
    return refresh_token(req.refresh_admin,res)

# user
@authRouter.post("/user/register",response_model=ResponseModel[RegisterResponse])
async def registerUser(user : RegisterBody,session : sessionDepedency) :
    return await authService.Register(user,session)