from fastapi import APIRouter, Depends, Request, Response

from ..domain.admin.auth.authModels import LoginModel,ResponseLoginAdmin
from ..domain.admin.auth.authService import login,refresh_token
from ..utils.sessionDepedency import sessionDepedency
from ..auth.dependAuthMiddleware.refreshTokenAdmin import refresh_token_auth
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..auth.dependAuthMiddleware.refreshTokenUser import refreshTokenUser

from ..models.responseModel import ResponseModel

from ..domain.auth import authService
from ..domain.auth.authModel import RegisterBody,RegisterResponse,LoginBody,LoginResponse,ResponseSelectRole,SelectRoleRequestBody,ResponseVerifyTdTokenBeforeRegister,ResponseGetUser,ResponseRefreshToken

from ..domain.auth.authModel import VerifyOTPBody

authRouter = APIRouter(prefix="/auth")
# admin
@authRouter.post("/admin/login",response_model=ResponseModel[ResponseLoginAdmin],tags=["AUTH/ADMIN"])
async def adminLogin(data : LoginModel,res : Response,session : sessionDepedency) :
    return await login(data,session,res)

@authRouter.post("/admin/refresh_token",dependencies=[Depends(refresh_token_auth)],response_model=ResponseModel[ResponseLoginAdmin],tags=["AUTH/ADMIN"])
def adminLogin(req : Request,res : Response) :
    return refresh_token(req.refresh_admin,res)

# user
@authRouter.post("/user/register",response_model=ResponseModel[RegisterResponse],tags=["AUTH/USER"])
async def registerUser(user : RegisterBody,session : sessionDepedency) :
    return await authService.Register(user,session)

@authRouter.post("/user/register/verifyIdToken",response_model=ResponseModel[ResponseVerifyTdTokenBeforeRegister],description="call before register using oauth2,used to verify the ID-token from oauth2 and check whether the account with the email you want to register is registered or not. error if already registered",tags=["AUTH/USER"])
async def verifyTokenBeforeRegister(id_token : str,session : sessionDepedency) :
    return await authService.verifyIdTokenBeforeRegister(id_token,session)

@authRouter.post("/user/register/googleOauth2",response_model=ResponseModel[RegisterResponse],description="the same as the usual register route but in registering with oauth2 the user does not need to verify his account and can be directly directed to the select role page",tags=["AUTH/USER"])
async def registerUser(user : RegisterBody,session : sessionDepedency) :
    return await authService.registergoogleOauth2(user,session)

@authRouter.post("/user/verifyAccount",responses={"200" : {
        "description": "when verify success",
        "content": {
            "application/json": {
                "example": [
                    {
                        "msg" : "verify account success" 
                    }
                ]
            }
        }
    }},dependencies=[Depends(userAuthDepends)],description="used to verify user account using OTP code",tags=["AUTH/USER"])
async def verifyuser(req : Request,OTP : VerifyOTPBody,session : sessionDepedency) :
    return await authService.verifyAccount(req.User,OTP.OTP,session)

@authRouter.post("/user/sendOTP",responses={"200" : {"content": {
                "application/json": {
                    "example" : {
                        "msg" : "Success,silahkan verifikasi akun anda dengan kode OTP yang telah dikirimkan melalui email"
                    }
                }
            }}},dependencies=[Depends(userAuthDepends)],description="used to resend the OTP code if the OTP has expired or something else",tags=["AUTH/USER"])
async def getUser(session : sessionDepedency,user : dict = Depends(GetUserDepends)) :
    return await authService.sendOtp(user["id"],session)

@authRouter.post("/user/login",responses={
    "200" : {
        "description": "if role equal null,redirect to page select role for select role and send token authorization from login token to select role",
            "content": {
                "application/json": {
                    "example" : {
                        "role": "null or servant or vendee",
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUwNjQ3MSIsInVzZXJuYW1lIjoiZGhpbGEiLCJpc1ZlcmlmeSI6dHJ1ZSwicm9sZSI6bnVsbH0.zJun5GnXXucJhSTFaPckGkeERUq5VagYiFZSHR03KgA",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUwNjQ3MSIsInVzZXJuYW1lIjoiZGhpbGEiLCJpc1ZlcmlmeSI6dHJ1ZSwicm9sZSI6bnVsbH0.ABjrgxoG8FYMYfAyq0xTCAPuYwwOJEY410w0Jh7KykE"
                    }
                }
            }
    }
},response_model=ResponseModel[LoginResponse],tags=["AUTH/USER"])
async def loginUser(loginBody : LoginBody,session : sessionDepedency) :
    return await authService.loginUser(loginBody,session)

@authRouter.post("/user/login/oauth2Google",response_model=ResponseModel[LoginResponse],description="used to log in using Google's Oauth2, the ID_token obtained by the frontend from Google is sent to the server and will be encoded to check whether the email is in the database. Make sure you send the ID_token",tags=["AUTH/USER"])
async def loginWithGoogleOauth2(id_token : str,session : sessionDepedency) :
    return await authService.loginWithGoogleOauth(id_token,session)

@authRouter.put("/select/role",response_model=ResponseModel[ResponseSelectRole],dependencies=[Depends(userAuthDepends)],tags=["AUTH/USER"])
async def selectRoleUser(role : SelectRoleRequestBody,session : sessionDepedency,user : dict = Depends(GetUserDepends)) :
    return await authService.selectRoleUser(user["id"],role,session)

@authRouter.get("/user",response_model=ResponseModel[ResponseGetUser],dependencies=[Depends(userAuthDepends)],description="""
used to get user data. if verify equal is false. the frontend can direct the user to the verification page and call send OTP to send the OTP. if the role on the user is equal null the frontend can direct the user to the select user role page.
This route is used before the user has a role""",tags=["AUTH/USER"])
async def getUser(session : sessionDepedency,user : dict = Depends(GetUserDepends)) :
    return await authService.getUser(user["id"],session)

@authRouter.get("/user/refresh_token",response_model=ResponseModel[ResponseRefreshToken],dependencies=[Depends(refreshTokenUser)],description="""
used to get user data. if verify equal is false. the frontend can direct the user to the verification page and call send OTP to send the OTP. if the role on the user is equal null the frontend can direct the user to the select user role page.
This route is used before the user has a role""",tags=["AUTH/USER"])
async def getUser(session : sessionDepedency,res : Response,user : dict = Depends(GetUserDepends)) :
    print("alit")
    return await authService.refresh_token(user,res,session)