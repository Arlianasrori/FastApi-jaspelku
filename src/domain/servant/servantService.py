from copy import deepcopy
from sqlalchemy import select,and_,func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .servantModel import AddDetailServant,ResponseAddUpdateDetailServant,ResponseProfilServant,ResponseGetServant,UpdateProfileServant,ResponseRatingsServant,ResponseGetRatingById,ResponseGetPesanans,ResponseGetPesananBYId
from ..models_domain.servantModel import ServantBase,ServantWithOutAlamat

from ...error.errorHandling import HttpException

from ...models.servantModel import Detail_Servant,Pelayanan_Category,Tujuan_Servant_Category,Time_Servant,Jadwal_Pelayanan,Tujuan_Servant
from ...models.userModel import User,Alamat_User
from ...models.pesananModel import Pesanan,Status_Pesanan_Enum
from ...models.ratingModel import Rating
from ...models.vendeeModel import Detail_Vendee

from python_random_strings import random_strings

from ...utils.updateTable import updateTable

# profile and detail
async def addDetailServant(id_user : str, detail_servant : AddDetailServant,session : AsyncSession) -> ResponseAddUpdateDetailServant :
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

async def getProfilServant(id_user : str,session : AsyncSession) -> ResponseProfilServant :
    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.tujuan_servant).options(joinedload(Tujuan_Servant.tujuan_servant_category)),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant))
    statementGetServant = await session.execute(select(User).options(joinedload(User.alamat),moreDetailServantQueryOption).where(User.id == id_user))
    findDetailServant = statementGetServant.scalars().first()

    if not findDetailServant : 
        raise HttpException(404,"servant tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : findDetailServant
    }

async def updateProfileServant(id_user : str,updateServant : UpdateProfileServant,session : AsyncSession) -> ResponseAddUpdateDetailServant :
    statementGetServant = await session.execute(select(User).options(joinedload(User.servant)).where(User.id == id_user))
    getUser = statementGetServant.scalars().first()

    if not getUser :
        raise HttpException(404,"servant tidak ditemukan")
    
    if updateServant.id_pelayanan :
        statementPelayananCategory = await session.execute(select(Pelayanan_Category).where(Pelayanan_Category.id == updateServant.id_pelayanan))
        findPelayananCategory = statementPelayananCategory.scalars().first()
        if not findPelayananCategory :
            raise HttpException(status=404,message="pelayanan tidak ditemukan")
        getUser.servant.id_pelayanan = updateServant.id_pelayanan

    if updateServant.timeServant :
        statementTimeServant = await session.execute(select(Time_Servant).where(Time_Servant.id_detail_servant == getUser.servant.id))
        findTimeServant = statementTimeServant.scalars().first()
        if not findTimeServant :
            raise HttpException(status=404,message="time servant tidak ditemukan")
        findTimeServant.time = updateServant.timeServant

    if updateServant.deskripsi :
        getUser.servant.deskripsi = updateServant.deskripsi

    if updateServant.jadwal :
        jadwalCopy = updateServant.jadwal.copy()

        for jadwal in jadwalCopy :
            print(jadwal)
            jadwalDump = jadwal.model_dump()
            if jadwalDump["isDelete"] :
                statementGetJadwal = await session.execute(select(Jadwal_Pelayanan).where(and_(Jadwal_Pelayanan.day == jadwalDump["day"],Jadwal_Pelayanan.id_detail_servant == getUser.servant.id))) 
                getJadwal = statementGetJadwal.scalars().first()
                await session.delete(getJadwal)
            else :
                jadwalMapping = {"id" : str(random_strings.random_digits(6)),"day" : jadwalDump["day"],"id_detail_servant" : getUser.servant.id} 
                session.add(Jadwal_Pelayanan(**jadwalMapping))
    
    if updateServant.alamat :
        statementGetAlamat = await session.execute(select(Alamat_User).where(Alamat_User.id_user == id_user))
        getAlamat = statementGetAlamat.scalars().first()
        updateTable(updateServant.alamat,getAlamat)

    await session.commit()

    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.tujuan_servant).options(joinedload(Tujuan_Servant.tujuan_servant_category)),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant))
    statementGetServant = await session.execute(select(User).options(joinedload(User.alamat),moreDetailServantQueryOption).where(User.id == id_user))
    findDetailServant = statementGetServant.scalars().first()

    return {
        "msg" : "success",
        "data" : findDetailServant
    }

# home
async def getDetailProfileServant(id_user : str,session : AsyncSession) :
    moreDetailServantQueryOption = joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.tujuan_servant).options(joinedload(Tujuan_Servant.tujuan_servant_category)),joinedload(Detail_Servant.jadwal_pelayanan),joinedload(Detail_Servant.time_servant))
    statementGetServant = await session.execute(select(User,func.avg(Rating.rating).label("total rating")).select_from(User).join_from(User,Detail_Servant,User.id == Detail_Servant.id_servant,full=True).join_from(Detail_Servant,Rating,Rating.id_detail_servant == Detail_Servant.id,full=True).group_by(User,Detail_Servant).options(joinedload(User.alamat),moreDetailServantQueryOption).where(User.id == id_user))
    findDetailServant = statementGetServant.first()

    servantDict = findDetailServant._asdict()

    servant = servantDict["User"]

    statementGetStatisticPesanan = await session.execute(select(func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("selesai"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.pengajuan).label("pengajuan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.proses).label("proses"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_servant).label("membatalkan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_vendee).label("dibatalkan"),func.count(Pesanan.id).label("total_pesanan"))
    .filter(Pesanan.id_detail_servant == servant.servant.id))

    findAnalisis = statementGetStatisticPesanan.first()

    # move total rating and statistik penjualan to detail servant on user field
    # print?(servant.__dict__)
    servant.__dict__["servant"].__dict__.update({"rating" : servantDict["total rating"] if servantDict["total rating"] else 0 ,"statistik_penjualan" : findAnalisis._asdict()})
    print(findAnalisis._asdict())

    return {
        "msg" : "success",
        "data" : servant.__dict__
    }

async def getRatings(id_user : str,session : AsyncSession) -> ResponseRatingsServant :
    statementGetServant = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).options(joinedload(Detail_Servant.ratings).joinedload(Rating.detail_vendee))).where(User.id == id_user))
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
    statementGetRating = await session.execute(select(Rating).options(vendeeLoad,servantLoad))
    getRating = statementGetRating.scalars().first()

    return {
        "msg" : "success",
        "data" : getRating
    }

# auth
async def getServant(id_user : str,session : AsyncSession) -> ResponseGetServant :
    statementGetServant = await session.execute(select(User).options(joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan)),joinedload(User.alamat)).where(User.id == id_user))
    getServant = statementGetServant.scalars().first()

    if not getServant :
        raise HttpException(404,"servant tidak ditemukan")
  
    return {
        "msg" : "success",
        "data" : getServant
    }

# pesanan
async def getPesanans(id_user : str,status_pesanan : Status_Pesanan_Enum | None,session : AsyncSession) -> ResponseGetPesanans :
    statementGetPesanan = await session.execute(select(User).options(joinedload(User.servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.pesanans.and_(Pesanan.status == status_pesanan.value))),joinedload(User.alamat)).where(User.id == id_user))
    getPesanans = statementGetPesanan.scalars().first()

    return {
        "msg" : "success",
        "data" : getPesanans
    }

async def getPesananById(id_pesanan : str,session : AsyncSession) -> ResponseGetPesananBYId :
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_vendee).joinedload(Detail_Vendee.vendee),joinedload(Pesanan.detail_servant)).where(Pesanan.id == id_pesanan))
    getPesanan = statementGetPesanan.scalars().first()

    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")
    
    statementGetUser = await session.execute(select(User).options(joinedload(User.servant).joinedload(Detail_Servant.pelayanan),joinedload(User.alamat)).where(User.id == getPesanan.detail_servant.id_servant))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")

    # add pesanan to getUser object in order to same with responseModel
    getUser.__dict__["servant"].__dict__.update({"pesanan" : deepcopy(getPesanan.__dict__)})

    return {
        "msg" : "success",
        "data" : getUser
    }

async def batalkanPesananServant(id_pesanan : str,id_user : str,session : AsyncSession) -> ResponseGetPesananBYId :
    statementGetUser = await session.execute(select(User).options(joinedload(User.servant).joinedload(Detail_Servant.pelayanan),joinedload(User.alamat)).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_vendee).joinedload(Detail_Vendee.vendee),joinedload(Pesanan.detail_servant)).where(and_(Pesanan.id == id_pesanan,Pesanan.id_detail_servant == getUser.servant.id)))
    getPesanan = statementGetPesanan.scalars().first()

    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")
    
    # check if status pesanan not proses,not can to cancel 
    if getPesanan.status != Status_Pesanan_Enum.proses :
        raise HttpException(400,"hanya pesanan dengan status proses yang bisa dibatalkan")

    getPesanan.status = Status_Pesanan_Enum.dibatalkan_servant.value
    # add pesanan to getUser object in order to same with responseModel
    getUserCopy = deepcopy(getUser)
    getUserCopy.__dict__["servant"].__dict__.update({"pesanan" : deepcopy(getPesanan.__dict__)})
    await session.commit()

    return {
        "msg" : "success",
        "data" : getUserCopy
    }

async def approvedPesananServant(id_pesanan : str,id_user : str,approved : bool,session : AsyncSession) -> ResponseGetPesananBYId :
    statementGetUser = await session.execute(select(User).options(joinedload(User.servant).joinedload(Detail_Servant.pelayanan),joinedload(User.alamat)).where(User.id == id_user))
    getUser = statementGetUser.scalars().first()

    if not getUser :
        raise HttpException(404,"user tidak ditemukan")
    
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_vendee).joinedload(Detail_Vendee.vendee),joinedload(Pesanan.detail_servant)).where(and_(Pesanan.id == id_pesanan,Pesanan.id_detail_servant == getUser.servant.id)))
    getPesanan = statementGetPesanan.scalars().first()

    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")
    
    # check if status pesanan not proses,not can to cancel 
    if getPesanan.status != Status_Pesanan_Enum.pengajuan :
        raise HttpException(400,"hanya pesanan dengan status pengajuan yang boleh diapproved")

    getPesanan.approved = approved
    if not approved :
        getPesanan.status = Status_Pesanan_Enum.rejected
    else :
        getPesanan.status = Status_Pesanan_Enum.proses
    # add pesanan to getUser object in order to same with responseModel
    getUserCopy = deepcopy(getUser)
    getUserCopy.__dict__["servant"].__dict__.update({"pesanan" : deepcopy(getPesanan.__dict__)})
    await session.commit()

    return {
        "msg" : "success",
        "data" : getUserCopy
    }


# READY ORDER
async def getReadyOrder(id_user : str,session : AsyncSession) -> ServantWithOutAlamat :
    statementGetDetailServant = await session.execute(select(User).options(joinedload(User.servant)).where(User.id == id_user))
    getDetailServant = statementGetDetailServant.scalars().first()

    if not getDetailServant :
        raise HttpException(404,"servant tidak ditemukan")
    return {
        "msg" : "success",
        "data" : getDetailServant
    }
    

async def updateReadyOrder(isReady : bool,id_user : str,session : AsyncSession) -> ServantBase :
    statementGetDetailServant = await session.execute(select(User).options(joinedload(User.alamat),joinedload(User.servant).joinedload(Detail_Servant.pelayanan)).where(User.id == id_user))
    getDetailServant = statementGetDetailServant.scalars().first()
    
    if not getDetailServant :
        raise HttpException(404,"user tidak ditemukan")
    
    getDetailServant.servant.ready_order = isReady
    getDetailServantCopy = deepcopy(getDetailServant)
    await session.commit()
    return {
        "msg" : "success",
        "data" : getDetailServantCopy
    }