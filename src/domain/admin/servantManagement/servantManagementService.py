from sqlalchemy.orm import Session
from ....models.servantModel import Pelayanan_Category
from .servantManagementModels import AddPelayananServantCategory,UpdatePelayananServantCategory,ResponsePelayananServantCategory
from ....error.errorHandling import HttpException


# pelayanan/jasa servant
def addPelayananServant(data : AddPelayananServantCategory,session : Session) -> ResponsePelayananServantCategory :
    dataMapping = data.model_dump()
    session.add(Pelayanan_Category(**dataMapping))
    session.commit()
    return {
        "msg" : "succes",
        "data" : data
    }

def updatePelayananServantCategory(id : str,data : UpdatePelayananServantCategory,session : Session) -> ResponsePelayananServantCategory :
    pelayanan_servant_category_query = session.query(Pelayanan_Category).where(Pelayanan_Category.id == id)

    pelayanan_servant_category_before = pelayanan_servant_category_query.first()

    if not pelayanan_servant_category_before :
        raise HttpException(status=404,message="pelayanan servanty category tidak ditemukan")
    
    pelayanan_servant_category_query.update({Pelayanan_Category.name : data.name})
    pelayana_servant = pelayanan_servant_category_query.first()
    session.commit()

    return {
        "msg" : "succes",
        "data" : pelayana_servant
    }

def deletePelayananServantCategory(id : str,session : Session) -> ResponsePelayananServantCategory :
    pelayanan_servant_category_query = session.query(Pelayanan_Category).where(Pelayanan_Category.id == id)

    pelayanan_servant_category_before = pelayanan_servant_category_query.first()

    if not pelayanan_servant_category_before :
        raise HttpException(status=404,message="pelayanan servanty category tidak ditemukan")
    
    pelayanan_servant_category_query.delete()
    pelayana_servant = pelayanan_servant_category_query.first()
    session.commit()

    return {
        "msg" : "succes",
        "data" : pelayana_servant
    }

def getAllPelayananServantCategory(session : Session) -> list[ResponsePelayananServantCategory] :
    pelayanan_servant_category = session.query(Pelayanan_Category).all()

    return {
        "msg" : "succes",
        "data" : pelayanan_servant_category
    }

def add_servant(session : Session) :
    pass

