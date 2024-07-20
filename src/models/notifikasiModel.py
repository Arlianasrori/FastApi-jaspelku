from ..db.database import Base
from sqlalchemy import Column,String,Boolean,Enum,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from enum import Enum as enum
import datetime

class NotifikasiCategory_Enunm(enum) :
    payment = "payment"
    info = "info"
    rating = "rating"

class Notifikasi_Category(Base) :
    __tablename__ = "notifikasi_category"

    id = Column(String,primary_key=True)
    name = Column(Enum(NotifikasiCategory_Enunm))

    notifikasi = relationship("Notifikasi",back_populates="notifikasi_category")

class Notifikasi(Base) :
    __tablename__ = "notifikasi"

    id = Column(String,primary_key=True)
    id_user = Column(String,ForeignKey("user.id"),nullable=True)
    notifikasi_category_id = Column(String,ForeignKey("notifikasi_category.id"))
    isi = Column(String)
    id_pesanan = Column(String,ForeignKey("pesanan.id"))

    notifikasi_category = relationship("Notifikasi_Category",back_populates="notifikasi")
    user = relationship("User",back_populates="notifikasi")
    pesanan = relationship("Pesanan",back_populates="notifikasi")
    notifikasi_read = relationship("Notifikasi_Read",back_populates="notifikasi")

class Notifikasi_Read(Base) :
    __tablename__ = "notifikasi_read"

    id = Column(String,primary_key=True)
    id_user = Column(String,ForeignKey("user.id"))
    id_notifikasi = Column(String,ForeignKey("notifikasi.id"))
    isRead = Column(Boolean)
    datetime = Column(DateTime,default=datetime.datetime.now())

    user = relationship("User",back_populates="notifikasi_read")
    notifikasi = relationship("Notifikasi",back_populates="notifikasi_read")