from ..db.database import Base
from sqlalchemy import Column, DateTime,String,Boolean,Enum,ForeignKey,Integer
from sqlalchemy.orm import relationship
from enum import Enum as enum
import datetime
# from .userModel import User

# Tabel perantara untuk hubungan many-to-many antara User dan room
class RoomUsers(Base):
    __tablename__ = "room_users"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user.id',ondelete="CASCADE"))
    room_id = Column(String, ForeignKey('room.id',ondelete="CASCADE"))

    room = relationship("Room",back_populates="roomUser")
    users = relationship("User",back_populates="roomUser")

class Room(Base):
    __tablename__ = "room"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    messages = relationship("Message", back_populates="room")
    roomUser = relationship("RoomUsers",back_populates="room")

# nmnmnm
class Message(Base) :
    __tablename__ = "message"

    id = Column(String,primary_key=True)
    message = Column(String,nullable=False)
    sender_id = Column(String,ForeignKey("user.id"),nullable=False)
    receiver_id = Column(String,ForeignKey("user.id"),nullable=False)
    is_read = Column(Boolean,nullable=False,default=False)
    created_at = Column(DateTime,nullable=False,default=datetime.datetime.utcnow())
    updated_at = Column(DateTime,nullable=False,default=datetime.datetime.utcnow(),onupdate=datetime.datetime.utcnow())
    room_id = Column(String,ForeignKey("room.id"),nullable=False)

    sender = relationship("User",back_populates="message_sender",foreign_keys=[sender_id])
    receiver = relationship("User",back_populates="message_receiver",foreign_keys=[receiver_id])
    media = relationship("MediaMessage",back_populates="message")
    room = relationship("Room",back_populates="messages")

    def __repr__(self) -> str:
        return f"Chat(id={self.id}, message={self.message}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, created_at={self.created_at}, updated_at={self.updated_at})"
    
class MediaMessage(Base):
    __tablename__ = "media_message"

    id = Column(String, primary_key=True)
    type = Column(String)  # Type of media (image, video, etc.)
    url = Column(String)
    message_id = Column(String, ForeignKey("message.id"))

    message = relationship("Message",back_populates="media")

    def __repr__(self) -> str:
        return f"media {self.message_id}-{self.type}-{self.url}"