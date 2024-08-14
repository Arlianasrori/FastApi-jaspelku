from ..db.database import Base
from sqlalchemy import Column, DateTime,String,Boolean,Enum,ForeignKey,Integer
from sqlalchemy.orm import relationship
from enum import Enum as enum

class RoleUser(enum) :
    servant = "servant"
    vendee = "vendee"

class User(Base) :
    __tablename__ = "user"

    id = Column(String,primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    no_telepon = Column(String(12),unique=True)
    password = Column(String,nullable=False)
    foto_profile = Column(String,nullable=True)
    isVerify = Column(Boolean,default=False)
    token_FCM = Column(String,nullable=True)
    role = Column(Enum(RoleUser),nullable=True)
    online = Column(Boolean,default=False)
    saldo  = Column(Integer,default=0)

    alamat = relationship("Alamat_User",back_populates="user",uselist=False,cascade="all")
    location_now = relationship("Location_Now",back_populates="user",cascade="all")
    servant = relationship("Detail_Servant",back_populates="servant",uselist=False,cascade="all")
    vendee = relationship("Detail_Vendee",back_populates="vendee",uselist=False,cascade="all")
    notifikasi = relationship("Notifikasi",back_populates="user",cascade="all")
    notifikasi_read = relationship("Notifikasi_Read",back_populates="user",cascade="all")
    OTP = relationship("OTPVerifyUser",backref="user",uselist=False,cascade="all")

class Alamat_User(Base) :
    __tablename__ = "alamat_user"

    id_user = Column(String,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    village = Column(String,nullable=False)
    subdistrick = Column(String,nullable=False)
    regency = Column(String,nullable=False)
    province = Column(String,nullable=False)
    country = Column(String,nullable=False)
    latitude = Column(String,nullable=True)
    longitude = Column(String,nullable=True)

    user = relationship("User",back_populates="alamat")

class Location_Now(Base) :
    __tablename__ = "location_now"

    id_user = Column(String,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    village = Column(String)
    subdistrick = Column(String)
    regency = Column(String)
    province = Column(String)
    country = Column(String)
    latitude = Column(String,nullable=True)
    longitude = Column(String,nullable=True)

    user = relationship("User",back_populates="location_now")

class OTPVerifyUser(Base) :
    __tablename__ = "OTP_User"
    id_user = Column(String,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    OTP = Column(String(6),nullable=False)
    expires = Column(DateTime,nullable=False)

class Tujuan_User_Category(Base) :
    __tablename__ = "tujuan_user_category"
    id = Column(String,primary_key=True)
    name = Column(String,nullable=False)

    tujuan_servant_category = relationship("Tujuan_Servant_Category",back_populates="tujuan_user_category",cascade="all")
    tujuan_vendee_category = relationship("Tujuan_Vendee_Category",back_populates="tujuan_user_category",cascade="all")