from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..utils.sessionDepedency import sessionDepedency
from ..models.responseModel import ResponseModel
from ..domain.generalUser import userService
from ..domain.generalUser.userModel import (
    ResponseUpdateFotoProfile,
    VerifyOtpForPasswordEmail,
    UpdatePassword,
    ResponsePasswordEmail,
    UpdateEmail,
    ResponseEmail
)
from ..domain.models_domain.notifikasiModel import NotifikasiwithUserRead,NotifikasiWithUser,NotifikasiBase

userRouter = APIRouter(prefix="/user",tags=["USER"])

@userRouter.patch("/foto_profile", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[ResponseUpdateFotoProfile])
async def update_foto_profile_user(
    user: Annotated[str, Depends(GetUserDepends)],
    foto_profile: UploadFile,
    session: sessionDepedency
):
    return await userService.update_foto_profile(user, foto_profile, session)

@userRouter.post("/password/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePasswordEmail)
async def send_otp_for_password(
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_password(user, session)

@userRouter.post("/passwordEmail/verifyOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePasswordEmail)
async def verify_otp_for_password_email(
    OTP: VerifyOtpForPasswordEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.verify_otp_for_password_email(OTP, user, session)

@userRouter.put("/password", dependencies=[Depends(userAuthDepends)], response_model=ResponsePasswordEmail)
async def update_password(
    password: UpdatePassword,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.update_password(password, user, session)

@userRouter.post("/email/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePasswordEmail)
async def send_otp_for_email(
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_email(user, session)

@userRouter.post("/email/cekEmail/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePasswordEmail)
async def send_otp_for_new_email(
    email: UpdateEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_new_email(email, user, session)

@userRouter.put("/email", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[ResponseEmail])
async def update_email(
    email: UpdateEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.update_email(email, user, session)

# notifikasi
@userRouter.get("/notifikasi", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[list[NotifikasiwithUserRead]],tags=["USER/NOTIFIKASI"])
async def getAllNotifikasi(user: Annotated[str, Depends(GetUserDepends)],session: sessionDepedency) :
    return await userService.getAllNotifikasi(user["id"],session)

@userRouter.get("/notifikasi/{id_notifikasi}", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[NotifikasiWithUser],tags=["USER/NOTIFIKASI"])
async def getNotifikasiById(id_notifikasi : str,user: Annotated[str, Depends(GetUserDepends)],session: sessionDepedency) :
    return await userService.getNotifikasiById(user["id"],id_notifikasi,session)

@userRouter.patch("/notifikasi/read/{id_notifikasi}", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[NotifikasiBase],tags=["USER/NOTIFIKASI"])
async def readNotifikasiById(id_notifikasi : str,user: Annotated[str, Depends(GetUserDepends)],session: sessionDepedency) :
    return await userService.readNotifikasi(user["id"],id_notifikasi,session)