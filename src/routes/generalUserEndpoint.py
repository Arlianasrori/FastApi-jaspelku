from fastapi import FastAPI,Depends,UploadFile
from sqlalchemy import select
from ..auth.dependAuthMiddleware.userAuthDepends import userAuthDepends
from ..auth.dependAuthMiddleware.getUserDepends import GetUserDepends
from ..models.userModel import User
from ..error.errorHandling import HttpException
from ..utils.sessionDepedency import sessionDepedency
from python_random_strings import random_strings
from typing import Annotated
import os
from pydantic import BaseModel
from ..models.responseModel import ResponseModel
from ..utils.sendOtp import sendOtp
from multiprocessing import Process
import datetime
from ..models.userModel import OTPVerifyUser
from sqlalchemy.orm import joinedload
from ..auth import bcrypt
from pydantic import field_validator

# foto profile
class ResponseUpdateFotoProfile(BaseModel) :
    id : str
    username : str
    email : str
    no_telepon : str
    foto_profile : str

# password
class VerifyOtpForPassword(BaseModel) :
    OTPcode : str

class UpdatePassword(BaseModel) :
    password : str

    @field_validator("password")
    def validate_password(cls, v) :
        if " " in v :
            raise ValueError("passowrd tidak bisa mengandung spasi")
        return v   
    
class ResponsePassword(BaseModel) :
    msg : str

fotoProfilePublicImage = os.getenv("DEV_FOTO_PROFILE_IMAGE_STORE")
fotoProfileBaseUrl = os.getenv("DEV_FOTO_PROFILE_IMAGE_BASE_URL")

def addGeneralUserEndpoint(app : FastAPI) :
    @app.patch("/user/foto_profile",dependencies=[Depends(userAuthDepends)],response_model=ResponseModel[ResponseUpdateFotoProfile],tags=["USER/PROFILE"])
    async def updateFotoProfileUser(user : Annotated[str,Depends(GetUserDepends)], foto_profile : UploadFile,session : sessionDepedency) :
        statementGetUser = await session.execute(select(User).where(User.id == user["id"]))
        getUser = statementGetUser.scalars().first() 
        if not getUser :
            raise HttpException(404,"user tidak ditemukan")

        extFile = foto_profile.filename.split(".")
        fileName = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(" ")[0]}.{extFile[len(extFile) - 1]}"
        fileNameSave = f"{fotoProfilePublicImage}{fileName}"

        userMapping = getUser.__dict__.copy()

        with open(fileNameSave , "wb") as f :
            f.write(foto_profile.file.read())
            getUser.foto_profile = f"{fotoProfileBaseUrl}/{fileName}"

        if userMapping["foto_profile"] :
            fileNamaDbSplit = userMapping["foto_profile"].split("/")
            fileNameDb = fileNamaDbSplit[len(fileNamaDbSplit) - 1]
            os.remove(f"{fotoProfilePublicImage}/{fileNameDb}")

        userCurrentDict =  getUser.__dict__.copy()
        await session.commit()
        return {
            "msg" : "success",
            "data" : userCurrentDict
        }

    @app.post("/user/password/sendOTP",dependencies=[Depends(userAuthDepends)],response_model=ResponsePassword,description="use this endpoint before update user password,to verify that the account really belongs to that user",tags=["USER/PASSWORD"])
    async def sendOtpForPassword(user : Annotated[str,Depends(GetUserDepends)],session : sessionDepedency) :
        statementGetUser = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == user["id"]))
        getUser = statementGetUser.scalars().first()

        if not getUser :
            raise HttpException(404,"user tidak ditemukan")
        
        OTPcode = str(random_strings.random_digits(6))
        delteExpires = datetime.timedelta(minutes=6)
        expires = datetime.datetime.now() + delteExpires
         # get mapping data and add to table OTP_user
        otpUserMapping = {
            "id_user" : getUser.id,
            "OTP" : OTPcode,
            "expires" : expires
        }
        if getUser.OTP :
            getUser.OTP.OTP = otpUserMapping["OTP"]
            getUser.OTP.expires = otpUserMapping["expires"]
        else :
            session.add(OTPVerifyUser(**otpUserMapping))
        await session.commit()
        userCopy = getUser.__dict__.copy()
        try :
            p1 = Process(target=sendOtp,args=(userCopy["email"],OTPcode,True))
            p1.start()
        except Exception as err:
            print(err)
        return {
            "msg" : "kode OTP sukses dikirim,silahkan cek email anda untuk melakukan verifikasi sebelum mengganti password"
        }
    
    @app.post("/user/password/verifyOTP",dependencies=[Depends(userAuthDepends)],response_model=ResponsePassword,description="use this endpoint to verify user OTP",tags=["USER/PASSWORD"])
    async def verifyOtpForPassword(OTP : VerifyOtpForPassword,user : Annotated[str,Depends(GetUserDepends)],session : sessionDepedency) :
        id_user = user["id"]
        statementGetUser = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == id_user))
        getUser = statementGetUser.scalars().first()

        if not getUser :
            raise HttpException(404,"user tidak ditemukan")
        
        # cek if otp from user equal with otp in database
        getOTP = getUser.OTP.__dict__
        print(getOTP["OTP"])
        if OTP.OTPcode == getOTP["OTP"] :
            now = datetime.datetime.now()
            if now > getOTP["expires"] :
                raise HttpException(400,"otp expires")
            return {
                "msg" : "verify account success"           
            }
        else :
            raise HttpException(400,"invalid OTP")
        
    @app.put("/user/password",dependencies=[Depends(userAuthDepends)],response_model=ResponsePassword,description="use this endpoint to update user password",tags=["USER/PASSWORD"])
    async def updatePassword(password : UpdatePassword,user : Annotated[str,Depends(GetUserDepends)],session : sessionDepedency) :
        statementGetUser = await session.execute(select(User).where(User.id == user["id"]))
        getUser = statementGetUser.scalars().first()

        if not getUser :
            raise HttpException(404,"user tidak ditemukan")

        hash_password = bcrypt.create_hash_password(password.password)
        getUser.password = hash_password
        await session.commit()

        return {
            "msg" : "update password success"
        }
