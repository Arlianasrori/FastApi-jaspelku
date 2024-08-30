from fastapi import APIRouter
# from ..domain.chat.chatModel 
from ..domain.chat import chatService
from ..domain.chat.chatModel import RoomList,MessageListRoom,RoomBase
from ..utils.sessionDepedency import sessionDepedency
from ..models.responseModel import ResponseModel

chatRouter = APIRouter(prefix="/user/chat")

@chatRouter.get("/room",response_model=ResponseModel[list[RoomList]],tags=["USER/CHAT"])
async def get_room(user_id : str,session : sessionDepedency) :
    return await chatService.get_room_list(user_id,session)

@chatRouter.get("/room/{room_id}",response_model=ResponseModel[RoomBase],tags=["USER/CHAT"])
async def get_room(room_id : str,session : sessionDepedency) :
    return await chatService.getRoomById("506471",room_id,session)

@chatRouter.get("/room/message/{room_id}",response_model=ResponseModel[list[MessageListRoom]],tags=["USER/CHAT"])
async def get_message_romm(room_id : str,session : sessionDepedency) :
    return await chatService.get_room_messages(room_id,session)