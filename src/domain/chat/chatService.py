from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_,func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ...models.userModel import User
from ...models.chatModel import RoomUsers,Room,Message,MediaMessage
from .chatModel import RoomList,MessageListRoom,RoomBase
from ...error.errorHandling import HttpException


async def get_room_list(user_id: str,session : AsyncSession) -> list[RoomList]:
    getUser = (await session.execute(select(User).filter(User.id == user_id).options(joinedload(User.roomUser).options(joinedload(RoomUsers.users),joinedload(RoomUsers.room))))).scalars().first()
    if not getUser:
        return []
    
    rooms = []
    for roomUser in getUser.roomUser:
        lastMessage = (await session.execute(select(Message).filter(Message.room_id == roomUser.room.id).order_by(Message.created_at.desc()))).scalar_one_or_none()

        getRoom = (await session.execute(select(RoomUsers).options(joinedload(RoomUsers.users)).filter(and_(RoomUsers.room_id == roomUser.room.id,RoomUsers.user_id != user_id)))).scalars().first()

        countNotReadMessage = (await session.execute(select(func.count(Message.id)).filter(and_(Message.room_id == roomUser.room.id,Message.receiver_id == user_id,Message.is_read == False)))).scalar_one()
        
        rooms.append({
            "id_room": roomUser.room.id,
            "toUserName": getRoom.users.__dict__["username"],
            "toUser_id" : getRoom.users.__dict__["id"],
            "last_message": lastMessage.message if lastMessage else "",
            "last_message_time": lastMessage.created_at if lastMessage else roomUser.room.updated_at,
            "not_read": countNotReadMessage
        })
    
    return {
            "msg" : "success",
            "data" :sorted(rooms, key=lambda x: x["last_message_time"], reverse=True)
        }

async def getRoomById(user_id : str,room_id : str,session : AsyncSession) -> RoomBase :
    getRoom = (await session.execute(select(Room).options(joinedload(Room.roomUser.and_(RoomUsers.user_id != user_id)).joinedload(RoomUsers.users)).where(Room.id == room_id))).scalars().first()

    if not getRoom :
        raise HttpException(404,"room tidak ditemukan")
    
    return {
        "msg" : "success",
        "data" : getRoom
    }
async def get_room_messages(room_id: str,session : AsyncSession) -> list[MessageListRoom]:
    getRoom = (await session.execute(select(Room).where(Room.id == room_id))).scalars().first()

    if not getRoom :
        raise HttpException(404,"room tidak ditemukan") 
    
    getMessageOnRoom = (await session.execute(select(Message).where(Message.room_id == room_id).order_by(Message.created_at.desc()))).scalars().all()

    return {
        "msg" : "success",
        "data" : getMessageOnRoom
    }


# async def send_message(conversation_id: str, sender_id: str, content: str,session : AsyncSession) :
    # new_message = Message(
    #     conversation_id=conversation_id,
    #     sender_id=sender_id,
    #     content=content
    # )
    # db.add(new_message)
    # await db.commit()
    
    # return {
    #     "id": new_message.id,
    #     "sender_id": new_message.sender_id,
    #     "content": new_message.content,
    #     "created_at": new_message.created_at,
    #     "is_read": new_message.is_read
    # }





# async def create_or_get_conversation(db, user_ids: List[str]) -> str:
#     subquery = select(user_conversation.c.conversation_id).filter(
#         user_conversation.c.user_id.in_(user_ids)
#     ).group_by(user_conversation.c.conversation_id).having(
#         func.count(distinct(user_conversation.c.user_id)) == len(user_ids)
#     ).subquery()

#     query = select(Conversation).filter(Conversation.id.in_(subquery))
#     result = await db.execute(query)
#     existing_conversation = result.scalar_one_or_none()

#     if existing_conversation:
#         return existing_conversation.id

#     new_conversation = Conversation()
#     db.add(new_conversation)
#     await db.flush()

#     for user_id in user_ids:
#         await db.execute(user_conversation.insert().values(
#             user_id=user_id,
#             conversation_id=new_conversation.id
#         ))

#     await db.commit()
#     return new_conversation.id

# def get_quick_replies() -> List[str]:
#     return [
#         "Saya telah menyelesaikan tugas!",
#         "Mohon tunggu sebentar!",
#         "Maaf. Saya tidak bisa melakukannya"
#     ]