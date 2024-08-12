from fastapi import Response
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,and_,or_
from sqlalchemy.orm import joinedload
from ...models.userModel import User,OTPVerifyUser
from .authModel import RegisterBody,RegisterResponse,LoginBody,LoginResponse,ResponseSelectRole,SelectRoleRequestBody,ResponseVerifyTdTokenBeforeRegister,ResponseGetUser,ResponseRefreshToken
from ...error.errorHandling import HttpException
from ...auth.createTokenUser import create_token_user
from python_random_strings import random_strings
from ...utils.sendOtp import sendOtp
from multiprocessing import Process
import datetime
from copy import deepcopy
from ...auth import bcrypt
from google.oauth2 import id_token
from google.auth.transport import requests
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


async def Register(user : RegisterBody,session : AsyncSession) -> RegisterResponse :
    # check if user already exist with email and nomor telepon
    statementCheckCountUserByEmailOrNo_Telepon = await session.execute(select(func.count(User.id)).where(or_(User.email == user.email,User.no_telepon == user.no_telepon)))
    getCountUserByEmailOrNo_Telepon = statementCheckCountUserByEmailOrNo_Telepon.scalar_one()

    if getCountUserByEmailOrNo_Telepon  > 0 :
        raise HttpException(400,"email atau nomor telepon telah digunakan")
    
    # mapping user BaseModel and add to database 
    userMapping = user.model_dump()
    hash_password = bcrypt.create_hash_password(userMapping["password"])
    userMapping.update({"id" : str(random_strings.random_digits(6)),"password" : hash_password})
    session.add(User(**userMapping))

    # create token for user
    token_payload = {"id" : userMapping["id"],"username" : userMapping["username"],"isVerify" : False,"role" : None}
    token = create_token_user(token_payload)

    # generate OTP and create on table OTP_User
    OTPCode = random_strings.random_digits(6)
    # get datetime now and plus with delta time,otp code expires after 6 minutes
    delteExpires = datetime.timedelta(minutes=6)
    expires = datetime.datetime.now() + delteExpires
    # get mapping data and add to table OTP_user
    
    otpUserMapping = {
        "id_user" : userMapping["id"] ,
        "OTP" : str(OTPCode),
        "expires" : expires
    }
    session.add(OTPVerifyUser(**otpUserMapping))

    await session.commit()

    # send otp to email using multithereading 
    try :
        p1 = Process(target=sendOtp,args=(user.email,OTPCode))
        p1.start()
    except Exception as err:
        print(err)

    return {
        "msg" : "register success,silahkan verifikasi akun anda dengan kode OTP yang telah dikirimkan melalui email",
        "data" : {
            **user.model_dump(exclude={"password"}),
            "id" : userMapping["id"],
            **token
        }
    }

async def verifyAccount(user : dict,otp : str,session : AsyncSession) :
    id_user = user["id"]
    statementGetUser = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    # cek if otp from user equal with otp in database
    getOTP = getUser.OTP.__dict__
    if otp == getOTP["OTP"] :
        now = datetime.datetime.now()
        if now > getOTP["expires"] :
            raise HttpException(400,"otp expires")
        
        getUser.isVerify = True
        await session.commit()
        return {
            "msg" : "verify account success"           
        }
    else :
        raise HttpException(400,"invalid OTP")

async def verifyIdTokenBeforeRegister(token_google_id : str,session : AsyncSession) -> ResponseVerifyTdTokenBeforeRegister:
    request = requests.Request()

    try :
        id_info = id_token.verify_oauth2_token(
            token_google_id, request, GOOGLE_CLIENT_ID)
    except Exception as err :
        raise HttpException(400,f"something wrong {err.args[0]}")
    
    if id_info['iss'] != 'https://accounts.google.com':
        raise HttpException('Wrong issuer.')

    userEmail = id_info["email"]
    statementGetUserByEmail = await session.execute(select(User).where(User.email == userEmail))
    getUser = statementGetUserByEmail.scalars().first()

    if getUser :
        raise HttpException(400,"akun telah ditambahkan")

    return {
        "msg" : "success",
        "data" : {
            "email" : id_info["email"],
            "username" : id_info["given_name"]
        }
    }
   
async def registergoogleOauth2(user : RegisterBody,session : AsyncSession) -> RegisterResponse :
    # check if user already exist with email and nomor telepon
    statementCheckCountUserByEmailOrNo_Telepon = await session.execute(select(func.count(User.id)).where(or_(User.email == user.email,User.no_telepon == user.no_telepon)))
    getCountUserByEmailOrNo_Telepon = statementCheckCountUserByEmailOrNo_Telepon.scalar_one()

    if getCountUserByEmailOrNo_Telepon  > 0 :
        raise HttpException(400,"email atau nomor telepon telah digunakan")
    
    # mapping user BaseModel and add to database 
    userMapping = user.model_dump()
    hash_password = bcrypt.create_hash_password(userMapping["password"])
    userMapping.update({"id" : str(random_strings.random_digits(6)),"password" : hash_password,"isVerify" : True})
    session.add(User(**userMapping))

    # create token for user
    token_payload = {"id" : userMapping["id"],"username" : userMapping["username"],"isVerify" : True,"role" : None}
    token = create_token_user(token_payload)

    await session.commit()
    return {
        "msg" : "register succes",
        "data" : {
            **user.model_dump(exclude={"password"}),
            "id" : userMapping["id"],
            **token
        }
    }
async def sendOtp(id_user : str,session : AsyncSession) :
    statementGetUser = await session.execute(select(User).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    # generate OTP and create on table OTP_User
    OTPCode = random_strings.random_digits(6)
    # get datetime now and plus with delta time,otp code expires after 6 minutes
    delteExpires = datetime.timedelta(minutes=6)
    expires = datetime.datetime.now() + delteExpires
    # get mapping data and add to table OTP_user
    statementGetVerifyUser = await session.execute(select(OTPVerifyUser).where(OTPVerifyUser.id_user == getUser.id))
    OTPUser = statementGetVerifyUser.scalars().first()

    otpUserMapping = {
        "id_user" : getUser.id,
        "OTP" : str(OTPCode),
        "expires" : expires
    }

    if not OTPUser :
        session.add(OTPVerifyUser(**otpUserMapping))
    else :
        OTPUser.OTP = otpUserMapping["OTP"]
        OTPUser.expires = expires

    await session.commit()
    
    # send otp to email using multithereading 
    try :
        p1 = Process(target=sendOtp,args=(getUser.email,OTPCode))
        p1.start()
    except Exception as err:
        print(err)
    
    return {
        "msg" : "Success,silahkan verifikasi akun anda dengan kode OTP yang telah dikirimkan melalui email"
    }

async def selectRoleUser(id_user : str,role : SelectRoleRequestBody,session : AsyncSession) -> ResponseSelectRole :
    statementGetUser = await session.execute(select(User).where(User.id == id_user))
    getUser = statementGetUser.scalars().one()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    getUser.role = role.role

    userMapping = deepcopy(getUser.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : userMapping
    }

async def loginUser(loginBody : LoginBody,session : AsyncSession) -> LoginResponse :
    statementGetUserByEmailNoHp = await session.execute(select(User).where(or_(User.email == loginBody.textBody,User.no_telepon == loginBody.textBody)))
    getUser = statementGetUserByEmailNoHp.scalars().first()

    if not getUser :
        raise HttpException(400,"email/nomor telepon or password wrong")
    
    if not getUser.isVerify :
        raise HttpException(400,"user belum melakukan verifikasi")
    
    isPassword = bcrypt.verify_hash_password(loginBody.password,getUser.password)
    if not isPassword :
        raise HttpException(400,"email/nomor telepon or password wrong") 
    
    # create token
    token_payload = {"id" : getUser.id,"username" : getUser.username,"isVerify" : getUser.isVerify,"role" : str(getUser.role)}
    token = create_token_user(token_payload)
    print("k")
    return {
        "msg" : "login success",
        "data" : {
            "role" : getUser.role,
            **token
        }
    }

async def loginWithGoogleOauth(token_google_id : str,session : AsyncSession) -> LoginResponse:
    request = requests.Request()

    try :
        id_info = id_token.verify_oauth2_token(
            token_google_id, request, GOOGLE_CLIENT_ID)
    except Exception as err :
        raise HttpException(400,f"something wrong {err.args[0]}")
    
    if id_info['iss'] != 'https://accounts.google.com':
        raise HttpException('Wrong issuer.')

    print(id_info)
    userEmail = id_info["email"]
    statementGetUserByEmail = await session.execute(select(User).where(User.email == userEmail))
    getUser = statementGetUserByEmail.scalars().first()

    if not getUser :
        raise HttpException(400,"login gagal,akun tidak ditemukan")
    
     # create token
    token_payload = {"id" : getUser.id,"username" : getUser.username,"isVerify" : getUser.isVerify,"role" : str(getUser.role)}
    token = create_token_user(token_payload)

    return {
        "msg" : "login success",
        "data" : {
            "role" : getUser.role,
            **token
        }
    }

async def getUser(id_user : str,session : AsyncSession) -> ResponseGetUser :
    statementGetUser = await session.execute(select(User).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    return {
        "msg" : "success",
        "data" : {
            "id" : getUser.id,
            "username" : getUser.username,
            "isVerify" : getUser.isVerify,
            "role" : getUser.role
        }
    }

async def refresh_token(data,res : Response,session : AsyncSession) -> ResponseRefreshToken :
    statementGetUser = await session.execute(select(User).where(User.id == data["id"]))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(401,"unauthorized")
    
    token_payload = {"id" : getUser.id,"username" : getUser.username,"isVerify" : getUser.isVerify,"role" : str(getUser.role)}
    token = create_token_user(token_payload)
    return {
        "msg" : "succes",
        "data" : token
    }