from fastapi import UploadFile
from sqlalchemy import select,and_
from sqlalchemy.orm import joinedload,subqueryload

from ...models.notifikasiModel import Notifikasi,Notifikasi_Read
from ...models.userModel import User, OTPVerifyUser
from .userModel import ResponseEmail, ResponseUpdateIsOnline,ResponseUpdateFotoProfile,ResponsePasswordEmail
from ..models_domain.notifikasiModel import NotifikasiwithUserRead,NotifikasiWithUser
from ...error.errorHandling import HttpException
from sqlalchemy.ext.asyncio import AsyncSession
from python_random_strings import random_strings
import os
import datetime
from multiprocessing import Process
from ...utils.sendOtp import sendOtp
from ...auth import bcrypt
from copy import deepcopy

# Ambil base URL dari environment
FOTO_PROFILE_PUBLIC_IMAGE = os.getenv("DEV_FOTO_PROFILE_IMAGE_STORE")
FOTO_PROFILE_BASE_URL = os.getenv("DEV_FOTO_PROFILE_IMAGE_BASE_URL")

async def update_foto_profile(user, foto_profile: UploadFile, session: AsyncSession) -> ResponseUpdateFotoProfile:
    statement_get_user = await session.execute(select(User).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()
    if not get_user:
        raise HttpException(404, "user tidak ditemukan")

    ext_file = foto_profile.filename.split(".")
    file_name = f"{random_strings.random_digits(12)}-{foto_profile.filename.split(' ')[0]}.{ext_file[-1]}"
    file_name_save = f"{FOTO_PROFILE_PUBLIC_IMAGE}{file_name}"

    user_mapping = get_user.__dict__.copy()

    with open(file_name_save, "wb") as f:
        f.write(foto_profile.file.read())
        get_user.foto_profile = f"{FOTO_PROFILE_BASE_URL}/{file_name}"

    if user_mapping["foto_profile"]:
        file_nama_db_split = user_mapping["foto_profile"].split("/")
        file_name_db = file_nama_db_split[-1]
        os.remove(f"{FOTO_PROFILE_PUBLIC_IMAGE}/{file_name_db}")

    user_current_dict = get_user.__dict__.copy()
    await session.commit()
    return {
        "msg": "success",
        "data": user_current_dict
    }

async def send_otp_for_password(user, session: AsyncSession) -> ResponsePasswordEmail:
    statement_get_user = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")
    
    otp_code = str(random_strings.random_digits(6))
    delta_expires = datetime.timedelta(minutes=6)
    expires = datetime.datetime.now() + delta_expires
    otp_user_mapping = {
        "id_user": get_user.id,
        "OTP": otp_code,
        "expires": expires
    }
    if get_user.OTP:
        get_user.OTP.OTP = otp_user_mapping["OTP"]
        get_user.OTP.expires = otp_user_mapping["expires"]
    else:
        session.add(OTPVerifyUser(**otp_user_mapping))
    await session.commit()
    user_copy = get_user.__dict__.copy()
    try:
        p1 = Process(target=sendOtp, args=(user_copy["email"], otp_code, True))
        p1.start()
    except Exception as err:
        print(err)
    return {
        "msg": "kode OTP sukses dikirim,silahkan cek email anda untuk melakukan verifikasi sebelum mengganti password"
    }

async def verify_otp_for_password_email(otp, user, session: AsyncSession) -> ResponsePasswordEmail:
    id_user = user["id"]
    statement_get_user = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == id_user))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")
    
    get_otp = get_user.OTP.__dict__
    if otp.OTPcode == get_otp["OTP"]:
        now = datetime.datetime.now()
        if now > get_otp["expires"]:
            raise HttpException(400, "otp expires")
        return {
            "msg": "verify account success"           
        }
    else:
        raise HttpException(400, "invalid OTP")

async def update_password(password, user, session: AsyncSession) -> ResponsePasswordEmail:
    statement_get_user = await session.execute(select(User).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")

    hash_password = bcrypt.create_hash_password(password.password)
    get_user.password = hash_password
    await session.commit()

    return {
        "msg": "update password success"
    }

async def send_otp_for_email(user, session: AsyncSession) -> ResponsePasswordEmail:
    statement_get_user = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")
    
    otp_code = str(random_strings.random_digits(6))
    delta_expires = datetime.timedelta(minutes=6)
    expires = datetime.datetime.now() + delta_expires
    otp_user_mapping = {
        "id_user": get_user.id,
        "OTP": otp_code,
        "expires": expires
    }
    if get_user.OTP:
        get_user.OTP.OTP = otp_user_mapping["OTP"]
        get_user.OTP.expires = otp_user_mapping["expires"]
    else:
        session.add(OTPVerifyUser(**otp_user_mapping))
    await session.commit()
    user_copy = get_user.__dict__.copy()
    try:
        p1 = Process(target=sendOtp, args=(user_copy["email"], otp_code))
        p1.start()
    except Exception as err:
        print(err)
    return {
        "msg": "kode OTP sukses dikirim,silahkan cek email anda untuk melakukan verifikasi sebelum mengganti email anda"
    }

async def send_otp_for_new_email(email, user, session: AsyncSession) -> ResponsePasswordEmail:
    statement_get_user = await session.execute(select(User).options(joinedload(User.OTP)).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")
    
    statement_get_user_by_email = await session.execute(select(User).where(User.email == email.email))
    get_user_by_email = statement_get_user_by_email.scalars().first()

    if get_user_by_email:
        raise HttpException(400, "email sudah ditambahkan")
    
    otp_code = str(random_strings.random_digits(6))
    delta_expires = datetime.timedelta(minutes=6)
    expires = datetime.datetime.now() + delta_expires
    otp_user_mapping = {
        "id_user": get_user.id,
        "OTP": otp_code,
        "expires": expires
    }
    if get_user.OTP:
        get_user.OTP.OTP = otp_user_mapping["OTP"]
        get_user.OTP.expires = otp_user_mapping["expires"]
    else:
        session.add(OTPVerifyUser(**otp_user_mapping))
    await session.commit()
    try:
        p1 = Process(target=sendOtp, args=(email.email, otp_code))
        p1.start()
    except Exception as err:
        print(err)
    return {
        "msg": "kode OTP sukses dikirim,silahkan cek email anda untuk melakukan verifikasi sebelum mengganti email anda"
    }

async def update_email(email, user, session: AsyncSession) -> ResponseEmail:
    statement_get_user = await session.execute(select(User).where(User.id == user["id"]))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")
    
    get_user.email = email.email
    get_user_copy = deepcopy(get_user)
    await session.commit()

    return {
        "msg": "update email success",
        "data": get_user_copy
    }

async def updateIsOnlineUser(user_id: int, is_online: bool, session: AsyncSession) -> ResponseUpdateIsOnline :
    statement_get_user = await session.execute(select(User).where(User.id == user_id))
    get_user = statement_get_user.scalars().first()

    if not get_user:
        raise HttpException(404, "user tidak ditemukan")

    get_user.online = is_online  # Memperbarui status isOnline
    await session.commit()

    return {
        "msg": "status online berhasil diperbarui",
        "data": {
            "user_id": user_id,
            "isOnline": is_online
        }
    }


async def getAllNotifikasi(user_id : str,session : AsyncSession) -> NotifikasiwithUserRead :
    getNotifikasi = (await session.execute(select(Notifikasi).options(joinedload(Notifikasi.user),subqueryload(Notifikasi.notifikasi_read.and_(Notifikasi_Read.id_user == user_id))).where(Notifikasi.id_user == user_id))).scalars().all()

    return {
        "msg" : "success",
        "data" : getNotifikasi
    }

async def getNotifikasiById(user_id : str,id_notifikasi : str,session : AsyncSession) -> NotifikasiWithUser :
    getNotifikasi = (await session.execute(select(Notifikasi).options(joinedload(Notifikasi.user)).where(and_(Notifikasi.id_user == user_id,Notifikasi.id == id_notifikasi)))).scalars().first()

    if not getNotifikasi :
        raise HttpException(404,"notifikasi tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : getNotifikasi
    }

async def readNotifikasi(user_id : str,id_notifikasi : str,session : AsyncSession) -> NotifikasiWithUser :
    getUser = (await session.execute(select(User).where(User.id == user_id))).scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    getNotifikasi = (await session.execute(select(Notifikasi).options(subqueryload(Notifikasi.notifikasi_read.and_(Notifikasi_Read.id_user == user_id))).where(Notifikasi.id == id_notifikasi))).scalars().first()

    if not getNotifikasi :
        raise HttpException(404,"notifikasi tidak ditemukan")
    
    if getNotifikasi.notifikasi_read :
        raise HttpException(400,"notifikasi sudah dibaca")
    
    notifikasi_read_payload = {
        "id" : str(random_strings.random_digits(6)),
        "id_user" : user_id,
        "id_notifikasi" : id_notifikasi,
        "isRead" : True
    }

    session.add(Notifikasi_Read(**notifikasi_read_payload))
    notifikasi_copy = deepcopy(getNotifikasi)
    await session.commit()

    return {
        "msg" : "notifikasi success dibaca",
        "data" : notifikasi_copy
    }