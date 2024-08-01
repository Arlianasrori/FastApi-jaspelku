from ....models.pesananModel import Pesanan,Order
from .pesananOrderManagementModel import OrderBase,PesananBase,PesananWithVendeeServant,OrdernWithVendeeServant,SearchPesanan
from ....models.vendeeModel import Detail_Vendee
from ....models.servantModel import Detail_Servant,Pelayanan_Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_,desc,func
from sqlalchemy.orm import joinedload
import datetime
import math

async def searchPesanan(page : int,search : SearchPesanan,session : AsyncSession) -> PesananBase :
    print(search.year)
    dateNow = datetime.datetime.now()
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
        print(queryStart)
        print(queryEnd)

    whereQuery = and_(Pesanan.datetime > queryStart,Pesanan.datetime < queryEnd,Pesanan.detail_servant.has(id_servant=search.servant) if search.servant else True,Pesanan.detail_vendee.has(id_vendee=search.vendee) if search.vendee else True,Pesanan.detail_servant.has(id_pelayanan = search.tugas) if search.tugas else True)
    # whereQueryPesanan = 
    statementGetAllPesanan = await session.execute(select(Pesanan).options(joinedload(Pesanan.detail_servant).options(joinedload(Detail_Servant.pelayanan)),joinedload(Pesanan.detail_vendee)).filter(whereQuery).order_by(desc(Pesanan.datetime)).limit(10).offset(10 * (page - 1)))
    allPesanan = statementGetAllPesanan.scalars().all()

    statementCountPage = await session.execute(select(func.count(Pesanan.id)).filter(whereQuery))
    # countPage = statementCountPage.scalar_one()
    countPage = math.ceil(statementCountPage.scalar_one() / 10)
    
    return {
        "msg" : "success",
        "pesanans" : allPesanan,
        "count_data" : len(allPesanan),
        "count_page" : countPage
    }