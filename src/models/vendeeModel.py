from ..db.database import Base
from sqlalchemy import Column,String,ForeignKey
from sqlalchemy.orm import relationship

class Detail_Vendee(Base) :
    __tablename__ = "detail_vendee"
    id = Column(String,primary_key=True)
    id_vendee = Column(String,ForeignKey("user.id"))
    deksripsi = Column(String)

    vendee = relationship("User",back_populates="vendee")
    tujuan_vendee = relationship("Tujuan_Vendee",back_populates="detail_vendee")
    ratings = relationship("Rating",back_populates="detail_vendee")
    pesanans = relationship("Pesanan",back_populates="detail_vendee")
    orders = relationship("Order",back_populates="detail_vendee")

class Tujuan_Vendee_Category(Base) :
    __tablename__ = "tujuan_vendee_category"

    id = Column(String,primary_key=True)
    id_tujuan_user_category = Column(String,ForeignKey("tujuan_user_category.id"))
    isi = Column(String)

    tujuan_user_category = relationship("Tujuan_User_Category",back_populates="tujuan_vendee_category")
    tujuan_vendee = relationship("Tujuan_Vendee",back_populates="tujuan_vendee_category")

class Tujuan_Vendee(Base) :
    __tablename__ = "tujuan_vendee"
    id = Column(String,primary_key=True)
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id"))
    id_tujuan_vendee_category = Column(String,ForeignKey("tujuan_vendee_category.id"))

    detail_vendee = relationship("Detail_Vendee",back_populates="tujuan_vendee")
    tujuan_vendee_category = relationship("Tujuan_Vendee_Category",back_populates="tujuan_vendee")
