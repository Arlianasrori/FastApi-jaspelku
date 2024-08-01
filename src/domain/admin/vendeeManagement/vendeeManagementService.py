from sqlalchemy.ext.asyncio import AsyncSession
from .vendeeManagementModel import VendeeBase,AddVendee,AddAlamat,AddDetailVendee,Updatevendee,UpdateAlamat,UpdateDetailVendee,MoreVendee,SearchVendeeResponse,SearchVendee,TujuanVendeeCategoryBase,AddTujuanVendeeCategory,UpdateTujuanVendeeCategory
from sqlalchemy import select,or_,and_,func
from sqlalchemy.orm import joinedload
from ....utils.updateTable import updateTable
from ....models.userModel import RoleUser, User,Alamat_User,Tujuan_User_Category
from ....models.vendeeModel import Detail_Vendee,Tujuan_Vendee_Category
from ....error.errorHandling import HttpException
from python_random_strings import random_strings
from copy import deepcopy
from types import NoneType
import asyncio
import math

async def add_vendee(vendee : AddVendee,alamat_vendee : AddAlamat,detail_vendee : AddDetailVendee, session : AsyncSession) -> VendeeBase :
    statementUser = await session.execute(select(User).where(or_(User.email == vendee.email,User.no_telepon == vendee.no_telepon)))
    findUser = statementUser.scalars().first()
    if findUser :
        raise HttpException(status=400,message="email atau nomor telepon sudah digunakan")

    # add user with alamat
    vendeeMapping = vendee.model_dump()
    alamatMapping = alamat_vendee.model_dump()
    vendeeMapping.update({"id" : str(random_strings.random_digits(6))})
    alamatMapping.update({"id_user" : vendeeMapping["id"]})
    session.add(User(**vendeeMapping,alamat=Alamat_User(**alamatMapping)))

    statementDetailVendee = await session.execute(select(Detail_Vendee).where(Detail_Vendee.id_vendee == vendeeMapping["id"]))
    findDetailVendee = statementDetailVendee.scalars().first()
    # if detail vendee exist,update detail vendee for new value from user
    if findDetailVendee :
        updateTable(detail_vendee,findDetailVendee)
        
    # add detail
    detailVendeeMapping = detail_vendee.model_dump()
    detailVendeeMapping.update({"id" : str(random_strings.random_digits(6)),"id_vendee" : vendeeMapping["id"]})
    session.add(Detail_Vendee(**detailVendeeMapping))

    await session.commit()
 
    statementVendee = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(User.id == vendeeMapping["id"]))
    
    findVendee = statementVendee.scalars().first()

    return {
        "msg" : "success",
        "data" : findVendee
    }

async def update_vendee(id : str,vendee : Updatevendee | None = None,alamat_vendee : UpdateAlamat | None = None,detail_vendee : UpdateDetailVendee | None = None, session : AsyncSession = None) -> VendeeBase : 
    statementUser = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(and_(User.id == id,User.role == RoleUser.vendee)))
    findUser = statementUser.scalars().first()

    if not findUser :
        raise HttpException(status=404,message="vendee tidak ditemukan")

    # update user
    if vendee :
        # check if email or no telepon from user id duplicate
        if (vendee.email != findUser.email and type(vendee.email) != NoneType) or (vendee.no_telepon != findUser.no_telepon and type(vendee.no_telepon) != NoneType) :
            statementUserByEmailNoTelepon = await session.execute(select(User).where(or_(User.email == vendee.email,User.no_telepon == vendee.no_telepon)))
            findUserByEmailNoTelepon = statementUserByEmailNoTelepon.scalars().first()

            if findUserByEmailNoTelepon :
                raise HttpException(400,"email atau nomor telepon sudah digunakan")
        updateTable(vendee,findUser)
    
    if alamat_vendee :
        updateTable(alamat_vendee,findUser.alamat)

    if detail_vendee :            
        updateTable(detail_vendee,findUser.vendee)

    vendee = deepcopy(findUser)
    
    await session.commit()

    return {
        "msg" : "success",
        "data" : vendee
    }

async def delete_vendee(id : str, session : AsyncSession) -> VendeeBase : 
    statementUser = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(and_(User.id == id,User.role == RoleUser.vendee)))
    findVendee = statementUser.scalars().first()

    if not findVendee :
        raise HttpException(status=404,message="vendee tidak ditemukan")

    await session.delete(findVendee)
    committask = asyncio.create_task(session.commit())
    vendee = deepcopy(findVendee)
    await committask

    return {
        "msg" : "success",
        "data" : vendee
    }

async def getAllvendees(session : AsyncSession) -> list[VendeeBase] :
    statement = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(User.role == RoleUser.vendee))
    allVendee = statement.scalars().all()
    return {
        "msg" : "success",
        "data" : allVendee
    }

async def searchvendee(page : int,filter : SearchVendee,session : AsyncSession) -> SearchVendeeResponse :
    searchFilterQuery = and_(User.username.like(f"%{filter.username}%") if filter.username else True,User.online == filter.online if filter.online else True,User.role == RoleUser.vendee)
    # 
    statement = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(searchFilterQuery).limit(10).offset(10 * (page - 1)))
    allVendee = statement.scalars().all()

    statementCountPage = await session.execute(select(func.count(User.id)).filter(searchFilterQuery))
    # countPage = statementCountPage.scalar_one()
    countPage = math.ceil(statementCountPage.scalar_one() / 10)
   
    return {
        "msg" : "success",
        "data" : {
            "vendee" : allVendee,
            "count_data" : len(allVendee),
            "count_page" : countPage
        }
    }

async def getvendeeById(id : str,session : AsyncSession) -> MoreVendee:
    moreDetailServantQueryOption = joinedload(User.vendee).options(joinedload(Detail_Vendee.pesanans),joinedload(Detail_Vendee.orders))
 
    statement = await session.execute(select(User).options(joinedload(User.alamat),moreDetailServantQueryOption).where(and_(User.id == id,User.role == RoleUser.vendee)))
    findDetailVendee = statement.scalars().first()
    
    if not findDetailVendee :
        raise HttpException(404,"vendee tidak ditemukan")
 
    return {
        "msg" : "succes",
        "data" : findDetailVendee
    }


# tujuan vendee category
async def addTujuanVendeeCategory(tujuan_vendee_category : AddTujuanVendeeCategory,session : AsyncSession) -> TujuanVendeeCategoryBase :
    statementTujuanUser = await session.execute(select(Tujuan_User_Category).where(Tujuan_User_Category.id == tujuan_vendee_category.id_tujuan_user_category))
    findTujuanUser = statementTujuanUser.scalars().first()

    # check if tujuan user is exist
    if not findTujuanUser :
        raise HttpException(404,"tujuan user category tidak ditemukan")
    
    tujuan_vendee_mapping = tujuan_vendee_category.model_dump()
    tujuan_vendee_mapping.update({"id" : str(random_strings.random_digits(6))})
    session.add(Tujuan_Vendee_Category(**tujuan_vendee_mapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : tujuan_vendee_mapping
    }

async def updateTujuanVendeeCategory(id : str,tujuan_vendee_category : UpdateTujuanVendeeCategory,session : AsyncSession) -> TujuanVendeeCategoryBase :
    statementGetTujuan = await session.execute(select(Tujuan_Vendee_Category).where(Tujuan_Vendee_Category.id == id))
    findTujuan = statementGetTujuan.scalars().first()

    if not findTujuan : 
        raise HttpException(404,"tujuan vendee category tidak ditemukan")
    
    updateTable(tujuan_vendee_category,findTujuan)
    tujuanVendee = deepcopy(findTujuan.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : tujuanVendee
    }

async def deleteTujuanvendeeCategory(id : str,session : AsyncSession) -> TujuanVendeeCategoryBase :
    statementGetTujuan = await session.execute(select(Tujuan_Vendee_Category).where(Tujuan_Vendee_Category.id == id))
    findTujuan = statementGetTujuan.scalars().first()

    if not findTujuan : 
        raise HttpException(404,"tujuan vendee category tidak ditemukan")
    
    await session.delete(findTujuan)
    tujuanVendee = deepcopy(findTujuan.__dict__)
    await session.commit()

    return {
        "msg" : "success",
        "data" : tujuanVendee
    }

async def getAllTujuanVendeeCategory(session : AsyncSession) -> list[TujuanVendeeCategoryBase] :
    statementGetTujuanvendee = await session.execute(select(Tujuan_Vendee_Category))
    allTujuanVendeeCategory = statementGetTujuanvendee.scalars().all()

    return {
        "msg" : "success",
        "data" : allTujuanVendeeCategory
    }

async def getTujuanVendeeCategoryById(id : str,session : AsyncSession) -> TujuanVendeeCategoryBase :
    statementGetTujuanVendee = await session.execute(select(Tujuan_Vendee_Category).where(Tujuan_Vendee_Category.id == id))
    tujuanVendeeCategory = statementGetTujuanVendee.scalars().first()

    if not tujuanVendeeCategory :
        raise HttpException(404,"tujuan servant category tidak ditemukan")

    return {
        "msg" : "success",
        "data" : tujuanVendeeCategory
    }