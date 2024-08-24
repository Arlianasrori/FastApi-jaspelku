from .socket import sio,online_users
from ..error.errorHandling import HttpException
from ..domain.models_domain.notifikasiModel import AddNotifikasiBody,NotifikasiWithUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from python_random_strings import random_strings

from ..models.userModel import User
from ..models.notifikasiModel import Notifikasi

async def sendNotification(id_user: str, data: AddNotifikasiBody, session: AsyncSession) -> NotifikasiWithUser:
    # Mengambil pengguna berdasarkan id_user
    getUser = (await session.execute(select(User).where(User.id == id_user))).scalars().first()

    # Memeriksa apakah pengguna ditemukan, jika tidak raise HttpException
    if not getUser:
        raise HttpException(400, "user tidak ditemukan")

    # Membuat salinan data dari objek AddNotifikasiBody
    dataMapping = data.model_dump()
    # Mencetak string acak berupa 6 digit
    print(random_strings.random_digits(6))
    # Menambahkan id_user dan id ke dataMapping
    dataMapping.update({"id_user": id_user, "id": str(random_strings.random_digits(6))})

    # Menambahkan objek Notifikasi ke sesi
    session.add(Notifikasi(**dataMapping))
    # Melakukan commit untuk menyimpan perubahan ke database
    await session.commit()

    # Looping untuk setiap pengguna online
    for user in online_users.items():
        sid, user = user

        # Memeriksa apakah user_id sama dengan id_user
        if user["user_id"] == id_user:
            # Mengambil notifikasi berdasarkan id dan menghilangkan beberapa atribut
            getNotifikasi = (await session.execute(select(Notifikasi).options(joinedload(Notifikasi.user)).where(Notifikasi.id == dataMapping["id"]))).scalars().first()
            notifDict: dict = getNotifikasi.__dict__
            userDict: dict = getNotifikasi.user.__dict__
            notifDict.pop("_sa_instance_state")
            userDict.pop("_sa_instance_state")
            userDict.pop("password")

            # Mengirim notifikasi menggunakan sio.emit() ke pengguna yang sesuai
            if getNotifikasi:
                await sio.emit("notifikasi", {
                    **notifDict,
                    "notifikasi_category_id": notifDict["notifikasi_category_id"].value,
                    "datetime": notifDict["datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                    "isRead": None,
                    "user": {
                        **userDict,
                        "role": userDict["role"].value,
                    }
                }, sid)