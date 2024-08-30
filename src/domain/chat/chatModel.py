from pydantic import BaseModel
from datetime import datetime as Datetime
from ..models_domain.userModel import UserBase

class RoomList(BaseModel) :
    id_room : str
    toUserName : str
    toUser_id : str
    last_message : str
    last_message_time : Datetime
    not_read : int

class RoomUserBase(BaseModel) :
    id : str
    user_id : str
    room_id : str
    users : UserBase

class RoomBase(BaseModel) :
    id : str
    created_at : Datetime
    updated_at : Datetime
    roomUser : list[RoomUserBase]

class MessageListRoom(BaseModel) :
    id : str
    message : str
    sender_id : str
    receiver_id : str
    is_read : bool
    created_at : Datetime
    updated_at : Datetime
    room_id : str
# class MediaBaseMessage(BaseModel) :

# class SendMessageBody(BaseModel) :
#     receiver_id : str
#     content : str
#     media : 


# send message
# cara send multiple file