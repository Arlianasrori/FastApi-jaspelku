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

    id = Column(String,primary_key=True)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"))
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id"))
    processing_time = Column(DateTime,default=datetime.datetime.now())
    datetime = Column(DateTime,default=datetime.datetime.now())
    additional_information = Column(String,nullable=True)
    order_estimate = Column(String)
    status = Column(Enum(Status_Pesanan_Enum))
    tugas = Column(String)
    total_price = Column(Integer)
    price_outside = Column(Integer)
    other_price = Column(Integer)
    isPay = Column(Boolean,default=False)
    approved = Column(Boolean,default=False)
    allowPayLater = Column(Boolean,default=False)
    isPayLater = Column(Boolean,default=False)

    detail_servant = relationship("Detail_Servant",back_populates="pesanans")
    detail_vendee = relationship("Detail_Vendee",back_populates="pesanans")
    order = relationship("Order",back_populates="pesanan")
    notifikasi = relationship("Notifikasi",back_populates="pesanan")

class Order(Base) :
    __tablename__ = "order"
    
    id = Column(String,primary_key=True)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"))
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id"))
    id_pesanan = Column(String,ForeignKey("pesanan.id"))
    payment_using = Column(String)
    price  = Column(Integer) 
    dateTime  = Column(DateTime,default=datetime.datetime.now())

    detail_servant = relationship("Detail_Servant",back_populates="orders")
    detail_vendee = relationship("Detail_Vendee",back_populates="orders")
    pesanan = relationship("Pesanan",back_populates="order")