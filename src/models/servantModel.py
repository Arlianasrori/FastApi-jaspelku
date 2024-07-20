from ..db.database import Base
from sqlalchemy import Column,String,Boolean,Enum,ForeignKey,Integer,UniqueConstraint
from sqlalchemy.orm import relationship
from enum import Enum as enum

class DayEnum(enum) :
    senin = "senin"
    selasa = "selasa"
    rabu = "rabu"
    kamis = "kamis"
    jumat = "jumat"
    sabtu = "sabtu"
    minggu = "minggu"

class Pelayanan_Category(Base) :
    __tablename__ = "pelayanan_category"
    id = Column(String,primary_key=True)
    name = Column(String)

    detail_servant = relationship("Detail_Servant",back_populates="pelayanan")

class Detail_Servant(Base) :
    __tablename__ = "detail_servant"

    id = Column(String,primary_key=True)
    id_servant = Column(String,ForeignKey("user.id"))
    deksripsi = Column(String,nullable=True)
    saldo  = Column(Integer,default=0)
    ready_order = Column(Boolean,default=False)
    id_pelayanan = Column(String,ForeignKey("pelayanan_category.id"))

    servant = relationship("User",back_populates="servant")
    pelayanan = relationship("Pelayanan_Category",back_populates="detail_servant")
    tujuan_servant = relationship("Tujuan_Servant",back_populates="detail_servant")
    jadwal_pelayanan = relationship("Jadwal_Pelayanan",back_populates="detail_servant")
    time_servant = relationship("Time_Servant",back_populates="detail_servant")
    ratings = relationship("Rating",back_populates="detail_servant")
    pesanans = relationship("Pesanan",back_populates="detail_servant")
    orders = relationship("Order",back_populates="detail_servant")

class Tujuan_Servant_Category(Base) :
    __tablename__ = "tujuan_servant_category"
    id = Column(String,primary_key=True)
    id_tujuan_user_category = Column(String,ForeignKey("tujuan_user_category.id"))
    isi = Column(String)

    tujuan_user_category = relationship("Tujuan_user_category",back_populates="tujuan_servant_category")
    tujuan_servant = relationship("Tujuan_Servant",back_populates="tujuan_servant_category")

class Tujuan_Servant(Base) :
    __tablename__ = "tujuan_servant"
    id = Column(String,primary_key=True)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"))
    id_tujuan_servant_category = Column(String,ForeignKey("tujuan_servant_category.id"))

    tujuan_servant_category = relationship("Tujuan_Servant_Category",back_populates="tujuan_servant")
    detail_servant = relationship("Detail_Servant",back_populates="tujuan_servant")

class Jadwal_Pelayanan(Base) : 
    __tablename__ = "jadwal_pelayanan"
    id = Column(String,primary_key=True)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"))
    day = Column(Enum(DayEnum))

    detail_servant = relationship("Detail_Servant",back_populates="jadwal_pelayanan")

    UniqueConstraint("id_detail_servant","day")

class Time_Servant(Base) :
    __tablename__ = "time_servant"
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"),primary_key=True)
    time = Column(String)

    detail_servant = relationship("Detail_Servant",back_populates="time_servant")
