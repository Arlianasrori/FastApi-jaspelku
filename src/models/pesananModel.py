from ..db.database import Base
from sqlalchemy import Column,String,Boolean,Enum,ForeignKey,Integer,DateTime
from sqlalchemy.orm import relationship
from enum import Enum as enum
import datetime

class Status_Pesanan_Enum(enum) :
    pengajuan = "pengajuan"
    proses = "proses"
    dibatalkan_vendee = "dibatalkan_vendee"
    dibatalkan_servant = "dibatalkan_servant"
    selesai = "selesai"

class Pesanan(Base) :
    __tablename__ = "pesanan"

    id = Column(String,primary_key=True,nullable=False)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id",ondelete="CASCADE"),nullable=False)
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id",ondelete="CASCADE"),nullable=False)
    processing_time = Column(DateTime,default=datetime.datetime.now(),nullable=False)
    datetime = Column(DateTime,default=datetime.datetime.now(),nullable=False)
    additional_information = Column(String,nullable=True)
    order_estimate = Column(String,nullable=False)
    status = Column(Enum(Status_Pesanan_Enum),nullable=False)
    tugas = Column(String,nullable=False)
    total_price = Column(Integer,nullable=False)
    price_outside = Column(Integer,default=0)
    other_price = Column(Integer,default=0)
    isPay = Column(Boolean,default=False)
    approved = Column(Boolean,default=False)
    allowPayLater = Column(Boolean,default=False)
    isPayLater = Column(Boolean,default=False)

    detail_servant = relationship("Detail_Servant",back_populates="pesanans")
    detail_vendee = relationship("Detail_Vendee",back_populates="pesanans")
    order = relationship("Order",back_populates="pesanan",cascade="all")
    notifikasi = relationship("Notifikasi",back_populates="pesanan",cascade="all")

class Order(Base) :
    __tablename__ = "order"
    
    id = Column(String,primary_key=True,nullable=False)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id",ondelete="CASCADE"),nullable=False)
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id",ondelete="CASCADE"),nullable=False)
    id_pesanan = Column(String,ForeignKey("pesanan.id",ondelete="CASCADE"))
    payment_using = Column(String,nullable=False)
    price  = Column(Integer,nullable=False) 
    dateTime  = Column(DateTime,default=datetime.datetime.now(),nullable=False)

    detail_servant = relationship("Detail_Servant",back_populates="orders")
    detail_vendee = relationship("Detail_Vendee",back_populates="orders")
    pesanan = relationship("Pesanan",back_populates="order")