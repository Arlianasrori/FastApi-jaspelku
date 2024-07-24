from sqlalchemy.orm import Session
from .userManagementModels import AddUpdateTujuanUserCategory,ResponseTujuanUserCategory
from ....models.userModel import Tujuan_User_Category
from ....error.errorHandling import HttpException
# from python_random_strings import random_strings

def add_tujuan_user_category(data : AddUpdateTujuanUserCategory,session : Session) -> ResponseTujuanUserCategory:  
    dataCopy = data.model_dump()
    # dataCopy.update({"id" : str(random_strings.random_digits(6))})
    session.add(Tujuan_User_Category(**dataCopy))
    session.commit()
    return {
        "msg" : "succes",
        "data" : dataCopy
    }

def update_tujuan_user_category(id : str,data : AddUpdateTujuanUserCategory,session : Session) -> ResponseTujuanUserCategory:
    tujuan_user_category_query = session.query(Tujuan_User_Category).where(Tujuan_User_Category.id == id)

    tujuan_user_category_before = tujuan_user_category_query.first()

    if not tujuan_user_category_before :
        raise HttpException(status=404,message="tujuan user category tidak ditemukan")
    
    tujuan_user_category_query.update({Tujuan_User_Category.name : data.name})
    session.commit()
    return {
        "msg" : "succes",
        "data" : {
            "id" : id,
            "nama" : data.name
        }
    }

def delete_tujuan_user_category(id : str,session : Session) -> ResponseTujuanUserCategory:
    tujuan_user_category_query = session.query(Tujuan_User_Category).where(Tujuan_User_Category.id == id)

    tujuan_user_category_before = tujuan_user_category_query.first()

    if not tujuan_user_category_before :
        raise HttpException(status=404,message="tujuan user category tidak ditemukan")
    
    tujuan_user_category = tujuan_user_category_query.first()
    tujuan_user_category_query.delete()
    session.commit()
    return {
        "msg" : "succes",
        "data" : tujuan_user_category
    }

def getAll_tujuan_user_category(session : Session) -> list[ResponseTujuanUserCategory] :
    tujuan_user_categories = session.query(Tujuan_User_Category).all()
    print(tujuan_user_categories)
    return {
        "msg" : "succes",
        "data" : tujuan_user_categories
    }

