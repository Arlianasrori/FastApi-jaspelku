from sqlalchemy.ext.asyncio import AsyncSession
from .userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ....models.userModel import Tujuan_User_Category
from ....error.errorHandling import HttpException
from python_random_strings import random_strings
from sqlalchemy import select
from ....utils.updateTable import updateTable

async def add_tujuan_user_category(data : AddUpdateTujuanUserCategory,session : AsyncSession) -> ResponseTujuanUserCategory:  
    dataCopy = data.model_dump()
    dataCopy.update({"id" : str(random_strings.random_digits(6))})
    session.add(Tujuan_User_Category(**dataCopy))
    await session.commit()
    return {
        "msg" : "succes",
        "data" : dataCopy
    }

async def update_tujuan_user_category(id : str,data : AddUpdateTujuanUserCategory,session : AsyncSession) -> ResponseTujuanUserCategory:
    tujuan_user_category_query = await session.execute(select(Tujuan_User_Category).where(Tujuan_User_Category.id == id))

    tujuan_user_category_before = tujuan_user_category_query.scalars().first()

    if not tujuan_user_category_before :
        raise HttpException(status=404,message="tujuan user category tidak ditemukan")
    
    updateTable(data,tujuan_user_category_before)
    print("tes bg")
    
    await session.commit()
    return {
        "msg" : "succes",
        "data" : {
            "id" : id,
            "name" : data.name
        }
    }

async def delete_tujuan_user_category(id : str,session : AsyncSession) -> ResponseTujuanUserCategory:
    statementTujuanUserCategory = await session.execute(select(Tujuan_User_Category).where(Tujuan_User_Category.id == id))

    tujuan_user_category = statementTujuanUserCategory.scalars().first()

    if not tujuan_user_category :
        raise HttpException(status=404,message="tujuan user category tidak ditemukan")

    await session.delete(tujuan_user_category)
    await session.commit()
    return {
        "msg" : "succes",
        "data" : tujuan_user_category
    }

async def getAll_tujuan_user_category(session : AsyncSession) -> list[ResponseTujuanUserCategory] :
    statementTujuanUserCategory = await session.execute(select(Tujuan_User_Category))
    tujuan_user_categories = statementTujuanUserCategory.scalars().all()
    print(tujuan_user_categories)
    return {
        "msg" : "succes",
        "data" : tujuan_user_categories
    }

