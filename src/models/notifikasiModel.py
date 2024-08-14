from ..db.database import Base
from sqlalchemy import Column,String,Boolean,Enum,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from enum import Enum as enum
import datetime

class NotifikasiCategory_Enum(enum) :
    payment = "payment"
    info = "info"
    rating = "rating"
    pesanan = "pesanan"

class Notifikasi(Base) :
    __tablename__ = "notifikasi"

    id = Column(String,primary_key=True,nullable=False)
    id_user = Column(String,ForeignKey("user.id",ondelete="CASCADE"),nullable=True)
    notifikasi_category_id = Column(Enum(NotifikasiCategory_Enum),nullable=False)
    isi = Column(String,nullable=False)
    id_pesanan = Column(String,ForeignKey("pesanan.id",ondelete="CASCADE"),nullable=True)
    datetime = Column(DateTime,default=datetime.datetime.now())

    user = relationship("User",back_populates="notifikasi")
    pesanan = relationship("Pesanan",back_populates="notifikasi")
    notifikasi_read = relationship("Notifikasi_Read",back_populates="notifikasi",cascade="all")

class Notifikasi_Read(Base) :
    __tablename__ = "notifikasi_read"

    id = Column(String,primary_key=True,nullable=False)
    id_user = Column(String,ForeignKey("user.id"),nullable=False)
    id_notifikasi = Column(String,ForeignKey("notifikasi.id",ondelete="CASCADE"),nullable=False)
    isRead = Column(Boolean,default=True)

    user = relationship("User",back_populates="notifikasi_read")
    notifikasi = relationship("Notifikasi",back_populates="notifikasi_read")