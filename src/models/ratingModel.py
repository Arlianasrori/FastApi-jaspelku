from ..db.database import Base
from sqlalchemy import Column,String,Enum,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from enum import Enum as enum

class RatingEnum(enum) :
    satu = 1
    dua = 2
    tiga = 3
    empat = 4
    lima = 5

class Rating(Base) :
    __tablename__ = "rating"
    id = Column(String,primary_key=True)
    id_detail_servant = Column(String,ForeignKey("detail_servant.id"))
    id_detail_vendee = Column(String,ForeignKey("detail_vendee.id"))
    rating = Column(Enum(RatingEnum))
    isi = Column(String)

    detail_servant = relationship("Detail_Servant",back_populates="ratings")
    detail_vendee = relationship("Detail_Vendee",back_populates="ratings")

    UniqueConstraint("id_detail_servant","id_detail_vendee")