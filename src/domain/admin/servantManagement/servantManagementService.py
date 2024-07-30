import asyncio
import math
from operator import or_
from types import NoneType
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ....models.servantModel import Pelayanan_Category
from .servantManagementModels import AddPelayananServantCategory,UpdatePelayananServantCategory,ResponsePelayananServantCategory
from ....error.errorHandling import HttpException
from .servantManagementModels import ServantBase,AddServant,AddDetailservant,AddAlamat,UpdateAlamat,UpdateServant,UpdateDetailservant,SearchServant,SearchServantResponse,MoreServantBase
from ....models.userModel import User,Alamat_User,RoleUser
from ....models.servantModel import Detail_Servant
from ....models.ratingModel import Rating
from python_random_strings import random_strings
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, select
from sqlalchemy.sql import or_
from ....utils.updateTable import updateTable
from copy import deepcopy
from sqlalchemy import func

# pelayanan/jasa servant
async def addPelayananServant(data : AddPelayananServantCategory,session : AsyncSession) -> ResponsePelayananServantCategory :
    dataMapping = data.model_dump()
    dataMapping.update({"id" :  str(random_strings.random_digits(6))})
    session.add(Pelayanan_Category(**dataMapping))
    await session.commit()
    print(data)
    return {
        "msg" : "succes",
        "data" : dataMapping
    }

async def updatePelayananServantCategory(id : str,data : UpdatePelayananServantCategory,session : AsyncSession) -> ResponsePelayananServantCategory :
    pelayanan_servant_category_query = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == id))

    pelayanan_servant_category = pelayanan_servant_category_query.scalars().first()

    if not pelayanan_servant_category :
        raise HttpException(status=404,message="pelayanan servanty category tidak ditemukan")
    
    updateTable(data,pelayanan_servant_category)

    pelayanan = pelayanan_servant_category.__dict__.copy()

    await session.commit()

    return {
        "msg" : "succes",
        "data" : pelayanan
    }

async def deletePelayananServantCategory(id : str,session : Session) -> ResponsePelayananServantCategory :
    pelayanan_servant_category_query = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == id))

    pelayanan_servant_category = pelayanan_servant_category_query.scalars().first()

    if not pelayanan_servant_category :
        raise HttpException(status=404,message="pelayanan servanty category tidak ditemukan")

    pelayanan = pelayanan_servant_category.__dict__.copy()
    await session.delete(pelayanan_servant_category)

    await session.commit()

    return {
        "msg" : "succes",
        "data" : pelayanan
    }

async def getAllPelayananServantCategory(session : AsyncSession) -> list[ResponsePelayananServantCategory] :
    selectPelayanan = await session.execute(select(Pelayanan_Category))
    pelayanans = selectPelayanan.scalars().all()

    return {
        "msg" : "succes",
        "data" : pelayanans
    }


# servant

async def add_servant(servant : AddServant,alamat_servant : AddAlamat,detail_servant : AddDetailservant, session : AsyncSession) -> ServantBase :
    statementPelayananCategory = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == detail_servant.id_pelayanan))
    findPelayananCategory = statementPelayananCategory.scalars().first()
    if not findPelayananCategory :
        raise HttpException(status=404,message="pelayanan tidak ditemukan")
    
    statementUser = await session.execute(select(User).where(or_(User.email == servant.email,User.no_telepon == servant.no_telepon)))
    findUser = statementUser.scalars().first()
    if findUser :
        raise HttpException(status=404,message="email atau nomor telepon sudah digunakan")

    # add user with alamat
    servantMapping = servant.model_dump()
    alamatMapping = alamat_servant.model_dump()
    servantMapping.update({"id" : str(random_strings.random_digits(6))})
    alamatMapping.update({"id_user" : servantMapping["id"]})
    session.add(User(**servantMapping,alamat=Alamat_User(**alamatMapping)))

    statementDetailServant = await session.execute(select(Detail_Servant).where(Detail_Servant.id_servant == servantMapping["id"]))
    findDetailServant = statementDetailServant.scalars().first()
    # if detail servant exist,update detail servant for new value from user
    if findDetailServant :
        updateTable(detail_servant,findDetailServant)
        
    # add detail
    detailServantMapping = detail_servant.model_dump()
    detailServantMapping.update({"id" : str(random_strings.random_digits(6)),"id_servant" : servantMapping["id"]})
    session.add(Detail_Servant(**detailServantMapping))

    await session.commit()
 
    statementServant = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan))).where(User.id == servantMapping["id"]))
    
    findServant = statementServant.scalars().first()

    return {
        "msg" : "success",
        "data" : findServant
    }

async def update_servant(id : str,servant : UpdateServant | None = None,alamat_servant : UpdateAlamat | None = None,detail_servant : UpdateDetailservant | None = None, session : AsyncSession = None) -> ServantBase : 
    statementUser = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan))).where(and_(User.id == id,User.role == RoleUser.servant)))
    findUser = statementUser.scalars().first()

    if not findUser :
        raise HttpException(status=404,message="servant tidak ditemukan")

    # update user
    if servant :
        # check if email or no telepon from user id duplicate
        if (servant.email != findUser.email and type(servant.email) != NoneType) or (servant.no_telepon != findUser.no_telepon and type(servant.no_telepon) != NoneType) :
            statementUserByEmailNoTelepon = await session.execute(select(User).where(or_(User.email == servant.email,User.no_telepon == servant.no_telepon)))
            findUserByEmailNoTelepon = statementUserByEmailNoTelepon.scalars().first()

            if findUserByEmailNoTelepon :
                raise HttpException(400,"email atau nomor telepon sudah digunakan")
        updateTable(servant,findUser)
    
    if alamat_servant :
        updateTable(alamat_servant,findUser.alamat)

    if detail_servant : 
        if detail_servant.id_pelayanan :
            statementPelayananCategory = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == detail_servant.id_pelayanan))
            findPelayananCategory = statementPelayananCategory.scalars().first()
            if not findPelayananCategory :
                raise HttpException(status=404,message="pelayanan tidak ditemukan")
            
        updateTable(detail_servant,findUser.servant)

    servant = deepcopy(findUser)
    
    await session.commit()

    return {
        "msg" : "success",
        "data" : servant
    }

async def delete_servant(id : str, session : AsyncSession) -> ServantBase : 
    statementUser = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan))).where(and_(User.id == id,User.role == RoleUser.servant)))
    findServant = statementUser.scalars().first()

    if not findServant :
        raise HttpException(status=404,message="servant tidak ditemukan")

    await session.delete(findServant)
    committask = asyncio.create_task(session.commit())
    servant = deepcopy(findServant)
    await committask

    return {
        "msg" : "success",
        "data" : servant
    }

async def getAllServants(session : AsyncSession) -> list[ServantBase] :
    statement = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan))).where(User.role == RoleUser.servant))
    allServant = statement.scalars().all()
    print(allServant)
    return {
        "msg" : "success",
        "data" : allServant
    }

async def searchServant(page : int,filter : SearchServant,session : AsyncSession) -> SearchServantResponse :
    searchFilterQuery = and_(User.username.like(f"%{filter.username}%") if filter.username else True,User.online == filter.online if filter.online else True,User.servant.has(ready_order=filter.ready_order) if filter.ready_order else True,User.role == RoleUser.servant)
    # 
    statement = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan))).where(searchFilterQuery).limit(10).offset(10 * (page - 1)))
    allServant = statement.scalars().all()

    statementCountPage = await session.execute(select(func.count(User.id)).filter(searchFilterQuery))
    # countPage = statementCountPage.scalar_one()
    countPage = math.ceil(statementCountPage.scalar_one() / 10)
   
    return {
        "msg" : "success",
        "data" : {
            "servant" : allServant,
            "count_data" : len(allServant),
            "count_page" : countPage
        }
    }

async def getServantById(id : str,session : AsyncSession) -> MoreServantBase :
    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.tujuan_servant),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant),joinedload(Detail_Servant.pesanans),joinedload(Detail_Servant.orders))
 
    statement = await session.execute(select(User,func.avg(Rating.rating).label("total rating")).select_from(User).join_from(User,Detail_Servant,User.id == Detail_Servant.id_servant,full=True).join_from(Detail_Servant,Rating,Rating.id_detail_servant == Detail_Servant.id,full=True).group_by(User,Detail_Servant).options(joinedload(User.alamat),moreDetailServantQueryOption).where(and_(User.id == id,User.role == RoleUser.vendee)))
    findDetailServant = statement.first()
    
    if not findDetailServant :
        raise HttpException(404,"servant tidak ditemukan")
    
    servantDict = findDetailServant._asdict()

    servant = servantDict["User"]
    # move total rating to detail servant on user field
    servant.__dict__["servant"].__dict__.update({"rating" : servantDict["total rating"] if servantDict["total rating"] else 0 })
 
    return {
        "msg" : "succes",
        "data" : servant
    }