from ....error.errorHandling import HttpException
from ....models.pesananModel import Pesanan,Order,Status_Pesanan_Enum
from .pesananOrderManagementModel import SearchPesananOrder,SearchPesananResponse,StatisticPesanan,SearchOrderResponse,StatisticOrder,ResponseOverviewPesanan,ResponseOverviewOrder

from ...models_domain.pesananOrderModel import PesananWithVendeeServant,OrdernWithVendeeServant
from ....models.vendeeModel import Detail_Vendee
from ....models.servantModel import Detail_Servant
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_,desc,func
from sqlalchemy.orm import joinedload
import datetime
import math
import enum

class TypeWhereQueryEnum(enum.Enum) :
    pesanan = "pesanan"
    order = "order"
async def getWhereQueryPesanan(search : SearchPesananOrder,type : TypeWhereQueryEnum) : 
    dateNow = datetime.datetime.now()
    if type == TypeWhereQueryEnum.pesanan :
        allowFilterDate = False
        if search.year or search.month or search.day :
            allowFilterDate = True

            #for end 
            yearStart = search.year if search.year else dateNow.year
            monthStart = search.month if search.month else 1
            dayStart = search.day if search.day else 1

            # for start
            yearEnd = search.year if search.year else dateNow.year
            monthEnd = search.month if search.month else 12
            dayEnd= search.day if search.day else 31

            # print()
            queryStart = datetime.date(yearStart,monthStart,dayStart)
            queryEnd = datetime.date(yearEnd,monthEnd,dayEnd)
        
        # where date query
        whereDateQuery = and_(Pesanan.date > queryStart ,Pesanan.date < queryEnd) if allowFilterDate else True

        # where query
        whereQuery = and_(Pesanan.detail_servant.has(id_servant=search.servant) if search.servant else True,Pesanan.detail_vendee.has(id_vendee=search.vendee) if search.vendee else True,Pesanan.detail_servant.has(id_pelayanan = search.tugas) if search.tugas else True)

    elif type == TypeWhereQueryEnum.order :
        allowFilterDate = False
        if search.year or search.month or search.day :
            allowFilterDate = True

            #for end 
            yearStart = search.year if search.year else dateNow.year
            monthStart = search.month if search.month else 1
            dayStart = search.day if search.day else 1

            # for start
            yearEnd = search.year if search.year else dateNow.year
            monthEnd = search.month if search.month else 12
            dayEnd= search.day if search.day else 31

            # print()
            queryStart = datetime.date(yearStart,monthStart,dayStart)
            queryEnd = datetime.date(yearEnd,monthEnd,dayEnd)
        
        # where date query
        whereDateQuery = and_(Order.date > queryStart ,Order.date < queryEnd) if allowFilterDate else True

        # where query
        whereQuery = and_(Order.detail_servant.has(id_servant=search.servant) if search.servant else True,Order.detail_vendee.has(id_vendee=search.vendee) if search.vendee else True,Order.detail_servant.has(id_pelayanan = search.tugas) if search.tugas else True)
  
    return {
        "dateQuery" : whereDateQuery,
        "otherQuery" : whereQuery
    }
month = ["januari","februari","maret","april","mei","juni","juli","agustus","september","oktober","november","desember"]


# pesanan
async def searchPesanan(page : int,search : SearchPesananOrder,session : AsyncSession) -> SearchPesananResponse :
    # get where query
    whereQuery = await getWhereQueryPesanan(search,TypeWhereQueryEnum.pesanan)

    statementGetAllPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant)),joinedload(Pesanan.detail_vendee).options(joinedload(Detail_Vendee.vendee))).filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])).order_by(desc(Pesanan.date)).limit(10).offset(10 * (page - 1)))
    allPesanan = statementGetAllPesanan.scalars().all()

    statementCountPage = await session.execute(select(func.count(Pesanan.id)).filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])))
    # countPage = statementCountPage.scalar_one()
    countPage = math.ceil(statementCountPage.scalar_one() / 10)
    # print(allPesanan[0].__dict__["detail_servant"].__dict__)

    return {
        "msg" : "success",
        "data" : {
            "pesanans" : allPesanan,
            "count_data" : len(allPesanan),
            "count_page" : countPage
        }
    }

async def searchStatisticPesanan(search : SearchPesananOrder,session : AsyncSession) -> StatisticPesanan :
    # get where query
    whereQuery = await getWhereQueryPesanan(search,TypeWhereQueryEnum.pesanan)

    statementGetStatisticPesanan = await session.execute(select(func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("jumlah_pesanan_selesai"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.pengajuan).label("jumlah_pesanan_pengajuan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.proses).label("jumlah_pesanan_proses"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_servant).label("jumlah_pesanan_dibatalkan_servant"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_vendee).label("jumlah_pesanan_dibatalkan_vendee"),func.count(Pesanan.id).label("total_pesanan"),
    func.sum(Pesanan.price).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("total_pendapatan_from_pesanan"))
    .filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])))

    findAnalisis = statementGetStatisticPesanan.first()
    print(findAnalisis._asdict())

    return {
        "msg" : "success",
        "data" : findAnalisis._asdict()
    }

async def getStatisticPesananToday(session : AsyncSession) -> StatisticPesanan :
    today = datetime.datetime.today().date()

    statementGetStatisticPesanan = await session.execute(select(func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("jumlah_pesanan_selesai"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.pengajuan).label("jumlah_pesanan_pengajuan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.proses).label("jumlah_pesanan_proses"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_servant).label("jumlah_pesanan_dibatalkan_servant"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_vendee).label("jumlah_pesanan_dibatalkan_vendee"),func.count(Pesanan.id).label("total_pesanan"),
    func.sum(Pesanan.price).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("total_pendapatan_from_pesanan")).filter(Pesanan.date == today))

    getStatistic = statementGetStatisticPesanan.first()._asdict()

    return {
        "msg" : "success",
        "data" : getStatistic
    }

async def getPesananById(id : int,session : AsyncSession) -> PesananWithVendeeServant :
    statementGetPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant)),joinedload(Pesanan.detail_vendee).options(joinedload(Detail_Vendee.vendee))).where(Pesanan.id == id))

    getPesanan = statementGetPesanan.scalars().first()

    if not getPesanan :
        raise HttpException(404,"pesanan tidak ditemukan")

    return {
        "msg" : "success",
        "data" : getPesanan
    }

async def getOverviewPesananByYear(year : int,session : AsyncSession) -> ResponseOverviewPesanan :
    todayYear = datetime.datetime.now().year
    yearStart = datetime.date(year if year else todayYear,1,1)
    yearEnd = datetime.date(year if year else todayYear,12,31)

    statementGetStatisticPesanan = await session.execute(select(func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("jumlah_pesanan_selesai"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.pengajuan).label("jumlah_pesanan_pengajuan"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.proses).label("jumlah_pesanan_proses"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_servant).label("jumlah_pesanan_dibatalkan_servant"),func.count(Pesanan.id).filter(Pesanan.status == Status_Pesanan_Enum.dibatalkan_vendee).label("jumlah_pesanan_dibatalkan_vendee"),func.count(Pesanan.id).label("total_pesanan"),
    func.sum(Pesanan.price).filter(Pesanan.status == Status_Pesanan_Enum.selesai).label("total_pendapatan_from_pesanan"),
    Pesanan.date).filter(and_(Pesanan.date >= yearStart,Pesanan.date <= yearEnd)).group_by(Pesanan.date))

    allPesanan = statementGetStatisticPesanan.all()
    yearStart = datetime.datetime(year if year else todayYear,1,1)
    yearEnd = datetime.datetime(year if year else todayYear,12,31)

    pesananByMonth = {}
    for i in range(12) :
        monthStart = datetime.date(year if year else todayYear,i + 1,1)
        monthEnd = datetime.date(year if year else todayYear,i + 1,27)
        pMonth = filter(lambda p: p._asdict()["date"] >= monthStart and p._asdict()["date"] <= monthEnd,allPesanan)
        pListMonth = list(pMonth)

        jumlah_pesanan_selesai = 0
        jumlah_pesanan_pengajuan = 0
        jumlah_pesanan_proses = 0
        jumlah_pesanan_dibatalkan_servant = 0
        jumlah_pesanan_dibatalkan_vendee = 0
        total_pesanan = 0
        total_pendapatan_from_pesanan = 0 

        for k in pListMonth :
            kDict = k._asdict()
            jumlah_pesanan_selesai += kDict["jumlah_pesanan_selesai"]
            jumlah_pesanan_pengajuan += kDict["jumlah_pesanan_pengajuan"]
            jumlah_pesanan_proses += kDict["jumlah_pesanan_proses"]
            jumlah_pesanan_dibatalkan_servant += kDict["jumlah_pesanan_dibatalkan_servant"]
            jumlah_pesanan_dibatalkan_vendee += kDict["jumlah_pesanan_dibatalkan_vendee"]
            total_pesanan += kDict["total_pesanan"]
            if kDict["total_pendapatan_from_pesanan"] :
                total_pendapatan_from_pesanan += kDict["total_pendapatan_from_pesanan"]

        pesananByMonth.update({month[i] : {
            "jumlah_pesanan_selesai" : jumlah_pesanan_selesai,
            "jumlah_pesanan_pengajuan" : jumlah_pesanan_pengajuan,
            "jumlah_pesanan_proses" : jumlah_pesanan_proses,
            "jumlah_pesanan_dibatalkan_servant" : jumlah_pesanan_dibatalkan_servant,
            "jumlah_pesanan_dibatalkan_vendee" : jumlah_pesanan_dibatalkan_vendee,
            "total_pesanan" : total_pesanan,
            "total_pendapatan_from_pesanan" : total_pendapatan_from_pesanan
        }})
   
    return {
        "msg" : "success",
        "data" : pesananByMonth
    }


# order
async def searchOrder(page : int,search : SearchPesananOrder,session : AsyncSession) -> SearchOrderResponse :
    whereQuery = await getWhereQueryPesanan(search,TypeWhereQueryEnum.order)

    statementGetOrders = await session.execute(select(Order).options(joinedload(Order.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant)),joinedload(Order.detail_vendee).options(joinedload(Detail_Vendee.vendee)),joinedload(Order.pesanan)).filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])).order_by(desc(Order.date)).limit(10).offset(10 * (page - 1)))
    allOrder = statementGetOrders.scalars().all()

    statementCountPage = await session.execute(select(func.count(Order.id)).filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])))

    # countPage = statementCountPage.scalar_one()
    countPage = math.ceil(statementCountPage.scalar_one() / 10)
    
    return {
        "msg" : "success",
        "data" : {
            "orders" : allOrder,
            "count_data" : len(allOrder),
            "count_page" : countPage
        }
    }

async def searchstatisticOrder(search : SearchPesananOrder,session : AsyncSession) -> StatisticOrder :
    whereQuery = await getWhereQueryPesanan(search,TypeWhereQueryEnum.order)

    statementGetOrder = await session.execute(select(func.count(Order.id).label("total_order")
    ,func.sum(Order.price).label("total_price")
    ,func.count(Order.id).filter(Order.payment_using == "bni").label("jumlah_order_bni")).filter(and_(whereQuery["otherQuery"],whereQuery["dateQuery"])))

    allIOrder = statementGetOrder.first()
    print(allIOrder._asdict())

    # proses guys
    return {
        "msg" : "success",
        "data" : allIOrder._asdict()
    }

async def getOrderById(id: int,session : AsyncSession) -> OrdernWithVendeeServant:
    statementGetOrders = await session.execute(select(Order).options(joinedload(Order.detail_servant).options(joinedload(Detail_Servant.pelayanan),joinedload(Detail_Servant.servant)),joinedload(Order.detail_vendee).options(joinedload(Detail_Vendee.vendee)),joinedload(Order.pesanan)).where(Order.id == id))
    findOrder = statementGetOrders.scalars().first()

    if not findOrder :
        raise HttpException(404,"order tidak ditemukan")

    return {
        "msg" : "success",
        "data" : findOrder
    }

async def getOrderToday(session : AsyncSession) -> StatisticOrder :
    today = datetime.datetime.today().date()

    statementGetOrder = await session.execute(select(func.count(Order.id).label("total_order")
    ,func.count(Order.price).label("total_price")
    ,func.count(Order.id).filter(Order.payment_using == "bni").label("jumlah_order_bni")).filter(Order.date == today))

    allIOrder = statementGetOrder.first()

    # proses guys
    return {
        "msg" : "success",
        "data" : allIOrder._asdict()
    }

async def getOverviewOrderByYear(year : int,session : AsyncSession) ->  ResponseOverviewOrder:
    todayYear = datetime.datetime.now().year
    yearStart = datetime.date(year if year else todayYear,1,1)
    yearEnd = datetime.date(year if year else todayYear,12,31)

    statementGetOrder = await session.execute(select(func.count(Order.id).label("total_order")
    ,func.sum(Order.price).label("total_price")
    ,func.count(Order.id).filter(Order.payment_using == "bni").label("jumlah_order_bni"),
    Order.date).filter(and_(Order.date >= yearStart,Order.date <= yearEnd)).group_by(Order.date))

    allOrder = statementGetOrder.all()
    yearStart = datetime.datetime(year if year else todayYear,1,1)
    yearEnd = datetime.datetime(year if year else todayYear,12,31)

    orderByMonth = {}
    for i in range(12) :
        monthStart = datetime.date(year if year else todayYear,i + 1,1)
        monthEnd = datetime.date(year if year else todayYear,i + 1,27)
        pMonth = filter(lambda p: p._asdict()["date"] >= monthStart and p._asdict()["date"] <= monthEnd,allOrder)
        pListMonth = list(pMonth)

        total_order = 0
        total_price = 0
        jumlah_order_bni = 0

        for k in pListMonth :
            kDict = k._asdict()

            total_order += kDict["total_order"]
            total_price += kDict["total_price"]
            jumlah_order_bni += kDict["jumlah_order_bni"]

        orderByMonth.update({month[i] : {
            "total_order" : total_order,
            "total_price" : total_price,
            "jumlah_order_bni" : jumlah_order_bni
        }})
   
    return {
        "msg" : "success",
        "data" : orderByMonth
    }