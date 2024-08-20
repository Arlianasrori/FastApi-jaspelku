from sqlalchemy import select,func,and_,desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload,subqueryload

from ...models.vendeeModel import Detail_Vendee,Tujuan_Vendee_Category,Tujuan_Vendee
from ...models.userModel import User,Alamat_User
from ...models.servantModel import Detail_Servant, Jadwal_Pelayanan, Pelayanan_Category, Time_Servant 
from ...models.ratingModel import Rating
from ...models.pesananModel import Pesanan,Status_Pesanan_Enum

from ...error.errorHandling import HttpException

from ..models_domain.vendeeModel import VendeeBase

from .vendeeModel import AddDetailVendeeBody,UpdateDetailVendeeBody,ResponseAddUpdateDetailVendee,ResponseFilterServant,SearchServantQuery,ResponseDetailProfileServant,ResponseRatingsServant,ResponseGetRatingById,ResponseGetPesanans,ResponseGetPesananBYId,AddPesananBody,ResponseAddUpdatePesanan,AddRatingBody,ResponseAddUpdateRating,UpdateRatingBody

from python_random_strings import random_strings

from ...utils.updateTable import updateTable

from copy import deepcopy


# profile
async def AddDetailVendee(id_user : str,detail_vendee : AddDetailVendeeBody,session : AsyncSession) -> ResponseAddUpdateDetailVendee :
     # get detail vendee from database and send error if detail vendee exist
    statementGetDetailVendee = await session.execute(select(Detail_Vendee).where(Detail_Vendee.id_vendee == id_user))
    findDetailVendee = statementGetDetailVendee.scalars().first()

    if findDetailVendee :
        raise HttpException(400,"detail vendee sudah ditambahkan")
    
    # mapping detail vendee and add some field like id and id_vendee
    detail_vendeeMapping = detail_vendee.model_dump(exclude={"id_tujuan_vendee_categories","alamat"})
    detail_vendeeMapping.update({"id" : str(random_strings.random_digits(6)),"id_vendee" : id_user})

    # mapping alamat_vendee and add some field like id_user
    alamat_mapping = detail_vendee.alamat.model_dump()
    alamat_mapping.update({"id_user" : id_user})

     # looping id_tujuan_vendee_categories and get item
    id_tujuan_vendee_categories = []
    for id_tujuan_vendee_category in detail_vendee.id_tujuan_vendee_categories.copy() :
        # get tujuan vendee category and check exsiting tujuan vendee
        id_tujuan_vendee_category = id_tujuan_vendee_category.__dict__
        statementTujuanCategory = await session.execute(select(Tujuan_Vendee_Category).where(Tujuan_Vendee_Category.id == id_tujuan_vendee_category["id_tujuan_vendee_category"]))
        findTujuanVendeeCategory = statementTujuanCategory.scalars().first()

        if not findTujuanVendeeCategory :
            raise HttpException(status=404,message="tujuan tidak ditemukan")
        
        # mappping tujuan vendee and append to id_tujuan_vendee_categories list for add all later
        tujuan_vendeeMapping = {"id" : str(random_strings.random_digits(6)),"id_detail_vendee" : detail_vendeeMapping["id"],"id_tujuan_vendee_category" : id_tujuan_vendee_category["id_tujuan_vendee_category"]}
        id_tujuan_vendee_categories.append(Tujuan_Vendee(**tujuan_vendeeMapping))
    
    session.add(Detail_Vendee(**detail_vendeeMapping))
    session.add(Alamat_User(**alamat_mapping))
    session.add_all(id_tujuan_vendee_categories)

    await session.commit()

    statementGetVendeeDetail = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee).joinedload(Detail_Vendee.tujuan_vendee).joinedload(Tujuan_Vendee.tujuan_vendee_category)).where(User.id == id_user))
    getDetailvendee = statementGetVendeeDetail.scalars().first()

    return {
        "msg" : "success",
        "data" : getDetailvendee
    }

async def updateProfileVendee(id_user : str,detail_vendee : UpdateDetailVendeeBody,session : AsyncSession) -> ResponseAddUpdateDetailVendee :
     # get detail vendee from database and send error if detail vendee exist
    statementGetDetailVendee = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)).where(Detail_Vendee.id_vendee == id_user))
    findDetailVendee = statementGetDetailVendee.scalars().first()

    if not findDetailVendee or not findDetailVendee.vendee :
        raise HttpException(400,"vendee atau detail vendee tidak ditemukan")
    
    if detail_vendee.deskripsi or detail_vendee.work :
    # mapping detail vendee and add some field like id and id_vendee
        detail_vendeeMapping = detail_vendee.model_dump(exclude={"id_tujuan_vendee_categories","alamat"})
        detail_vendeeMapping.update({"id" : str(random_strings.random_digits(6)),"id_vendee" : id_user})
        updateTable(detail_vendee,findDetailVendee.vendee)
        

    # check if alamat is exist mapping and add id_user field
    if detail_vendee.alamat :
        alamat_mapping = detail_vendee.alamat.model_dump()
        alamat_mapping.update({"id_user" : id_user})
        updateTable(detail_vendee.alamat,findDetailVendee.alamat)

    await session.commit()

    statementGetVendeeDetail = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee).joinedload(Detail_Vendee.tujuan_vendee).joinedload(Tujuan_Vendee.tujuan_vendee_category)).where(User.id == id_user))
    getDetailvendee = statementGetVendeeDetail.scalars().first()

    return {
        "msg" : "success",
        "data" : getDetailvendee
    }


async def getProfileVendee(id_user : str,session : AsyncSession) -> VendeeBase :
    statementGetDetailVendee = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)))
    getVendee = statementGetDetailVendee.scalars().first()

    if not getVendee or not getVendee.vendee :
        raise HttpException(404,"user atau detail user tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : getVendee
    }

async def getVendee(id_user : str,session : AsyncSession) -> VendeeBase :
    statementGetDetailVendee = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.vendee)))
    getVendee = statementGetDetailVendee.scalars().first()

    if not getVendee or not getVendee.vendee :
        raise HttpException(404,"user atau detail user tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : getVendee
    }


# get servant
SELECT_SERVANT_QUERY_WITH_RATING = (select(User,Alamat_User,Detail_Servant,func.avg(Rating.rating).label("total rating")).select_from(User)
                                      .join_from(User,Detail_Servant,User.id == Detail_Servant.id_servant,full=True)
                                      .join_from(Detail_Servant,Rating,Rating.id_detail_servant == Detail_Servant.id,full=True)
                                      .join_from(User,Alamat_User,full=True)
                                      .join_from(Detail_Servant,Pelayanan_Category)
                                      .join_from(Detail_Servant,Time_Servant)
                                      .join_from(Detail_Servant,Jadwal_Pelayanan)
                                      .group_by(User,Detail_Servant,Alamat_User,Pelayanan_Category,Time_Servant,Jadwal_Pelayanan)
                                      .options(subqueryload(Detail_Servant.pelayanan),subqueryload(Detail_Servant.jadwal_pelayanan),subqueryload(Detail_Servant.time_servant))
                                      )

async def getServantFilter(page : int,search : SearchServantQuery,session : AsyncSession) -> ResponseFilterServant :
    statement = await session.execute(SELECT_SERVANT_QUERY_WITH_RATING.where(and_(User.role == "servant",User.username.ilike(f"%{search.username}%") if search.username else True,Detail_Servant.id_pelayanan == search.id_pelayanan if search.id_pelayanan else True)).limit(10).offset(10 * (page - 1)))
    findDetailServant = statement.all()

    # looping findDetailservant and get by dict every item and adjust it to the model response
    details = []
    for detail in findDetailServant :
        detailDict = detail._asdict()
        detailServantItem = {
            **detailDict["User"].__dict__,
            "alamat" : detailDict["Alamat_User"],
            "servant" : {
                **detailDict["Detail_Servant"].__dict__,
                "rating" : detailDict["total rating"] if detailDict["total rating"] else 0
            }
        }
        details.append(detailServantItem)


    return {
        "msg" : "success",
        "data" : details
    }

async def getServantByRating(page : int,session : AsyncSession) -> ResponseFilterServant :
    statement = await session.execute(SELECT_SERVANT_QUERY_WITH_RATING.limit(10).offset(10 * (page - 1)).order_by(desc(func.avg(Rating.rating))))
    findDetailServant = statement.all()

    # looping findDetailservant and get by dict every item and adjust it to the model response
    details = []
    for detail in findDetailServant :
        detailDict = detail._asdict()
        detailServantItem = {
            **detailDict["User"].__dict__,
            "alamat" : detailDict["Alamat_User"],
            "servant" : {
                **detailDict["Detail_Servant"].__dict__,
                "rating" : detailDict["total rating"] if detailDict["total rating"] else 0
            }
        }
        details.append(detailServantItem)


    return {
        "msg" : "success",
        "data" : details
    }

async def getServantById(id_servant : str,session : AsyncSession) -> ResponseDetailProfileServant : 
    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant))
    statementGetServant = await session.execute(select(User,func.avg(Rating.rating).label("total rating")).select_from(User).join_from(User,Detail_Servant,User.id == Detail_Servant.id_servant,full=True).join_from(Detail_Servant,Rating,Rating.id_detail_servant == Detail_Servant.id,full=True).group_by(User,Detail_Servant).options(joinedload(User.alamat),moreDetailServantQueryOption).where(User.id == id_servant))
    findDetailServant = statementGetServant.first()

    if not findDetailServant :
        raise HttpException(404,"servant tidak ditemukan")

    servantDict = findDetailServant._asdict()

    servant = servantDict["User"]

    statementGetStatisticPesanan = await session.execute(select(func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("selesai"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.pengajuan).label("pengajuan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.proses).label("proses"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_servant).label("membatalkan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_vendee).label("dibatalkan"),func.count(Pesanan.id).label("total_pesanan"))
    .filter(Pesanan.id_detail_servant == servant.servant.id))

    findAnalisis = statementGetStatisticPesanan.first()

    # move total rating and statistik penjualan to detail servant on user field
    servant.__dict__["servant"].__dict__.update({"rating" : servantDict["total rating"] if servantDict["total rating"] else 0 ,"statistik_penjualan" : findAnalisis._asdict()})

    return {
        "msg" : "success",
        "data" : servant.__dict__
    }

async def getRatingServant(id_servant : str,session : AsyncSession) -> ResponseRatingsServant :
    statementGetServant = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.ratings).joinedload(Rating.detail_vendee))).where(User.id == id_servant))
    getServantWithRating = statementGetServant.scalars().first()

    if not getServantWithRating :
        raise HttpException(404,"servant tidak ditemukan")

    return {
        "msg" : "success",
        "data" : getServantWithRating
    }

async def getRatingById(id_rating : str,session : AsyncSession) -> ResponseGetRatingById :
    vendeeLoad = joinedload(Rating.detail_vendee).options(joinedload(Detail_Vendee.vendee).options(joinedload(User.alamat)))
    servantLoad = joinedload(Rating.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant).options(joinedload(User.alamat)))
    statementGetRating = await session.execute(select(Rating).options(vendeeLoad,servantLoad).where(Rating.id == id_rating))
    getRating = statementGetRating.scalars().first()

    if not getRating :
        raise HttpException(404,"data rating tidak ditemukan")

    return {
        "msg" : "success",
        "data" : getRating
    }


# pesanan
async def getPesanans(id_user : str,status_pesanan : Status_Pesanan_Enum | None,session : AsyncSession) -> ResponseGetPesanans :
    statementGetPesanan = await session.execute(select(User).options(joinedload(User.vendee).options(joinedload(Detail_Vendee.pesanans.and_(Pesanan.status == status_pesanan.value if status_pesanan else True)).joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.servant),joinedload(Detail_Servant.pelayanan))),joinedload(User.alamat)).where(User.id == id_user))
    getPesanans = statementGetPesanan.scalars().first()

    return {
        "msg" : "success",
        "data" : getPesanans
    }

async def getPesananById(id_pesanan : str,session : AsyncSession) -> ResponseGetPesananBYId :
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.servant),joinedload(Detail_Servant.pelayanan)),joinedload(Pesanan.detail_vendee)).where(Pesanan.id == id_pesanan))
    getPesanan = statementGetPesanan.scalars().first()
    
    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")
    
    statementGetUser = await session.execute(select(User).options(joinedload(User.vendee),joinedload(User.alamat)).where(User.id == getPesanan.detail_vendee.id_vendee))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")

    # add pesanan to getUser object in order to same with responseModel
    getUser.__dict__["vendee"].__dict__.update({"pesanan" : deepcopy(getPesanan.__dict__)})

    return {
        "msg" : "success",
        "data" : getUser
    }


async def batalkanPesanan(id_pesanan : str,id_user : str,session : AsyncSession) -> ResponseGetPesananBYId :
    statementGetUser = await session.execute(select(User).options(joinedload(User.vendee),joinedload(User.alamat)).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.servant),joinedload(Detail_Servant.pelayanan)),joinedload(Pesanan.detail_vendee)).where(Pesanan.id == id_pesanan))
    getPesanan = statementGetPesanan.scalars().first()
    
    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")
    
    # check if status pesanan not proses,not can to cancel 
    if getPesanan.status != Status_Pesanan_Enum.pengajuan :
        raise HttpException(400,"hanya pesanan dengan status pengajuan yang bisa dibatalkan oleh vendee")

    getPesanan.status = Status_Pesanan_Enum.dibatalkan_vendee.value
    # add pesanan to getUser object in order to same with responseModel
    getUserCopy = deepcopy(getUser)
    getUserCopy.__dict__["vendee"].__dict__.update({"pesanan" : deepcopy(getPesanan.__dict__)})
    await session.commit()

    return {
        "msg" : "success",
        "data" : getUserCopy
    }

async def AddPesanan(id_user : str,pesanan : AddPesananBody,session : AsyncSession) -> ResponseAddUpdatePesanan :
    statementGetVendee = await session.execute(select(User).options(joinedload(User.vendee)).where(User.id == id_user))
    getVendee = statementGetVendee.scalars().first()
    if not getVendee :
        raise HttpException(404,"vendee tidak ditemukan")
    
    statementGetServant = await session.execute(select(User).options(joinedload(User.servant).joinedload(Detail_Servant.pelayanan)).where(User.id == pesanan.id_user_servant))
    getServant = statementGetServant.scalars().first()

    if not getServant :
        raise HttpException(404,"servant tidak ditemukan")
    
    pelayanan_servant_category_query = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == getServant.servant.id_pelayanan))

    pelayanan_servant_category = pelayanan_servant_category_query.scalars().first()

    if not pelayanan_servant_category :
        raise HttpException(status=404,message="pelayanan servanty category tidak ditemukan")
    
    pesananMapping = {  "id" : str(random_strings.random_digits(6)),
                        "id_detail_servant" : getServant.servant.id,
                        "id_detail_vendee" : getVendee.vendee.id,
                        "additional_information" : pesanan.additional_information,
                        "order_estimate" : pesanan.order_estimate,
                        "status" : Status_Pesanan_Enum.pengajuan.value,
                        "tugas" : pelayanan_servant_category.name,
                        "price" : pelayanan_servant_category.price
                    }
    
    session.add(Pesanan(**pesananMapping))
    await session.commit()

    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant).joinedload(User.alamat)),joinedload(Pesanan.detail_vendee).joinedload(Detail_Vendee.vendee).joinedload(User.alamat)).where(Pesanan.id == pesananMapping["id"]))
    getPenasan = statementGetPesanan.scalars().first()

    return {
        "msg" : "success",
        "data" : getPenasan
    }

async def addRating(id_user : str,rating : AddRatingBody,session : AsyncSession) -> ResponseAddUpdateRating :
    statementGetVendee = await session.execute(select(User).options(joinedload(User.vendee)).where(User.id == id_user))
    getVendee = statementGetVendee.scalars().first()
    if not getVendee :
        raise HttpException(404,"vendee tidak ditemukan")
    
    statementGetServant = await session.execute(select(User).options(joinedload(User.servant)).where(User.id == rating.id_user_servant))
    getServant = statementGetServant.scalars().first()

    if not getServant :
        raise HttpException(404,"servant tidak ditemukan")
    
    ratingMapping = rating.model_dump(exclude={"id_user_servant"})
    ratingMapping.update({"id" : str(random_strings.random_digits(6)),"id_detail_vendee" : getVendee.vendee.id,"id_detail_servant" : getServant.servant.id})
    session.add(Rating(**ratingMapping))
    await session.commit()

    return {
        "msg" : "success",
        "data" : ratingMapping
    }
async def updateRating(id_user : str,id_rating : str,rating : UpdateRatingBody,session : AsyncSession) -> ResponseAddUpdateRating :
    statementGetUser = await session.execute(select(User).options(joinedload(User.vendee)).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()
    if not getUser :
        raise HttpException(404,"vendee tidak ditemukan")
     
    statementGetRating = await session.execute(select(Rating).where(Rating.id == id_rating))
    getRating = statementGetRating.scalars().first()
    if not getRating :
        raise HttpException(404,"rating tidak ditemukan")
    updateTable(rating,getRating)
    await session.commit()

    statementGetRating = await session.execute(select(Rating).where(Rating.id == id_rating))
    getRating = statementGetRating.scalars().first()

    return {
        "msg" : "success",
        "data" : getRating
    }