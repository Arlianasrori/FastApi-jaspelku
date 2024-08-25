from ..db.database import Base
from sqlalchemy import Column, DateTime,String,Boolean,Enum,ForeignKey,Integer
from sqlalchemy.orm import relationship
from enum import Enum as enum
import datetime
# from .userModel import User

class Chat(Base) :
    __tablename__ = "chat"

    id = Column(String,primary_key=True)
    message = Column(String,nullable=False)
    sender_id = Column(String,ForeignKey("user.id"),nullable=False)
    receiver_id = Column(String,ForeignKey("user.id"),nullable=False)
    is_read = Column(Boolean,nullable=False,default=False)
    created_at = Column(DateTime,nullable=False,default=datetime.datetime.utcnow())
    updated_at = Column(DateTime,nullable=False,default=datetime.datetime.utcnow())

    sender = relationship("User",back_populates="chat_sender",foreign_keys=[sender_id])
    receiver = relationship("User",back_populates="chat_receiver",foreign_keys=[receiver_id])
    media = relationship("MediaChat",back_populates="chat")

    def __repr__(self) -> str:
        return f"Chat(id={self.id}, message={self.message}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, created_at={self.created_at}, updated_at={self.updated_at})"
    
class MediaChat(Base):
    __tablename__ = "media_chat"

    id = Column(String, primary_key=True)
    type = Column(String)  # Type of media (image, video, etc.)
    url = Column(String)
    chat_id = Column(String, ForeignKey("chat.id"))

    chat = relationship("Chat",back_populates="media")

    def __repr__(self) -> str:
        return f"media {self.chat_id}-{self.type}-{self.url}"