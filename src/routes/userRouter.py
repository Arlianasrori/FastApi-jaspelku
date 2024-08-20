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
    ResponsePassword,
    UpdateEmail,
    ResponseEmail
)

userRouter = APIRouter(tags=["USER"])

@userRouter.patch("/user/foto_profile", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[ResponseUpdateFotoProfile])
async def update_foto_profile_user(
    user: Annotated[str, Depends(GetUserDepends)],
    foto_profile: UploadFile,
    session: sessionDepedency
):
    return await userService.update_foto_profile(user, foto_profile, session)

@userRouter.post("/user/password/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePassword)
async def send_otp_for_password(
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_password(user, session)

@userRouter.post("/user/passwordEmail/verifyOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePassword)
async def verify_otp_for_password_email(
    OTP: VerifyOtpForPasswordEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.verify_otp_for_password_email(OTP, user, session)

@userRouter.put("/user/password", dependencies=[Depends(userAuthDepends)], response_model=ResponsePassword)
async def update_password(
    password: UpdatePassword,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.update_password(password, user, session)

@userRouter.post("/user/email/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePassword)
async def send_otp_for_email(
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_email(user, session)

@userRouter.post("/user/email/cekEmail/sendOTP", dependencies=[Depends(userAuthDepends)], response_model=ResponsePassword)
async def send_otp_for_new_email(
    email: UpdateEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.send_otp_for_new_email(email, user, session)

@userRouter.put("/user/email", dependencies=[Depends(userAuthDepends)], response_model=ResponseModel[ResponseEmail])
async def update_email(
    email: UpdateEmail,
    user: Annotated[str, Depends(GetUserDepends)],
    session: sessionDepedency
):
    return await userService.update_email(email, user, session)