from ..db.database import Base
from sqlalchemy import Column,String,Boolean,Enum,ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as enum

class RoleUser(enum) :
    servant = "servant"
    vendee = "vendee"

class User(Base) :
    __tablename__ = "user"

    id = Column(String,primary_key=True)
    username = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    foto_profile = Column(String,nullable=True)
    isVerify = Column(Boolean,default=False)
    token_FCM = Column(String,nullable=True)
    role = Column(Enum(RoleUser),nullable=True)
    online = Column(Boolean,default=False)

    alamat = relationship("Alamat_User",back_populates="user")
    location_now = relationship("Location_Now",back_populates="user")
    servant = relationship("Detail_Servant",back_populates="servant")
    vendee = relationship("Detail_Vendee",back_populates="vendee")
    notifikasi = relationship("Notifikasi",back_populates="user")
    notifikasi_read = relationship("Notifikasi_Read",back_populates="user")

class Alamat_User(Base) :
    __tablename__ = "alamat_user"

    id_user = Column(String,ForeignKey("user.id"),primary_key=True)
    village = Column(String)
    subdistrick = Column(String)
    regency = Column(String)
    province = Column(String)
    country = Column(String)
    latitude = Column(String,nullable=True)
    longitude = Column(String,nullable=True)

    user = relationship("User",back_populates="alamat")

class Location_Now(Base) :
    __tablename__ = "location_now"

    id_user = Column(String,ForeignKey("user.id"),primary_key=True)
    village = Column(String)
    subdistrick = Column(String)
    regency = Column(String)
    province = Column(String)
    country = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    user = relationship("User",back_populates="location_now")

class Tujuan_User_Category(Base) :
    __tablename__ = "tujuan_user_category"
    id = Column(String,primary_key=True)
    nama = Column(String)

    tujuan_servant_category = relationship("Tujuan_Servant_Category",back_populates="tujuan_user_category")
    tujuan_vendee_category = relationship("Tujuan_Vendee_Category",back_populates="tujuan_user_category")