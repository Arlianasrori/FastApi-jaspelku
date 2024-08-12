from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .servantModel import AddDetailServant,ResponseAddDetailServant

from ...error.errorHandling import HttpException

from ...models.servantModel import Detail_Servant,Pelayanan_Category,Tujuan_Servant_Category,Time_Servant,Jadwal_Pelayanan,Tujuan_Servant
from ...models.userModel import User,Alamat_User

from python_random_strings import random_strings

async def addDetailServant(id_user : str, detail_servant : AddDetailServant,session : AsyncSession) -> ResponseAddDetailServant :
    # get detail servant from database and send error if detail servant exist
    statementGetDetailServant = await session.execute(select(Detail_Servant).where(Detail_Servant.id_servant == id_user))
    findDetailServant = statementGetDetailServant.scalars().first()

    if findDetailServant :
        raise HttpException(400,"detail servant sudah ditambahkan")
    # find pelayana servant category and send error if not exist
    statementPelayananCategory = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == detail_servant.id_pelayanan))
    findPelayananCategory = statementPelayananCategory.scalars().first()
    if not findPelayananCategory :
        raise HttpException(status=404,message="pelayanan tidak ditemukan")
    
    # mapping detail servant and add some field like id and id_servant
    detail_servantMapping = detail_servant.model_dump(exclude={"timeServant","alamat","jadwal","id_tujuan_servant_category"})
    detail_servantMapping.update({"id" : str(random_strings.random_digits(6)),"id_servant" : id_user})

    # mapping time servant and add some field like id_detail_servant
    timeServantMapping = {"id_detail_servant" : detail_servantMapping["id"],"time" : detail_servant.timeServant}

    # mapping alamat_servant and add some field like id_user
    alamat_mapping = detail_servant.alamat.model_dump()
    alamat_mapping.update({"id_user" : id_user})

    # find tujuan servant category
    statementPelayananCategory = await session.execute(select(Tujuan_Servant_Category).where(Tujuan_Servant_Category.id == detail_servant.id_tujuan_servant_category))
    findTujuanServantCategory = statementPelayananCategory.scalars().first()
    if not findTujuanServantCategory :
        raise HttpException(status=404,message="tujuan tidak ditemukan")
    
    tujuan_servantMapping = {"id" : str(random_strings.random_digits(6)),"id_detail_servant" : detail_servantMapping["id"],"id_tujuan_servant_category" : detail_servant.id_tujuan_servant_category}

    session.add(Detail_Servant(**detail_servantMapping,time_servant = Time_Servant(**timeServantMapping),tujuan_servant=Tujuan_Servant(**tujuan_servantMapping)))

    session.add(Alamat_User(**alamat_mapping))

    # mapping jadwal servant and add id_detail on every items
    jadwalCopy = detail_servant.jadwal.copy() 
    jadwalMapping = [] 
    for i in range(len(jadwalCopy)) :     
        jadwalItem = jadwalCopy[i].model_dump()
        jadwalItem.update({"id" : str(random_strings.random_digits(6)),"id_detail_servant" : detail_servantMapping["id"]})
        jadwalMapping.append(Jadwal_Pelayanan(**jadwalItem))

    session.add_all(jadwalMapping)

    await session.commit()

    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.tujuan_servant).options(joinedload(Tujuan_Servant.tujuan_servant_category)),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant))
    statementGetServant = await session.execute(select(User).options(joinedload(User.alamat),moreDetailServantQueryOption).where(User.id == id_user))
    findDetailServant = statementGetServant.scalars().first()

    return {
        "msg" : "success",
        "data" : findDetailServant
    }