from fastapi import Request
from ...models.userModel import RoleUser
from ...error.errorHandling import HttpException
async def servantAuthDepends(req : Request) :
    user = req.User
    print(user)

    if user["role"] != RoleUser.servant :
        raise HttpException(403,"forbidden,role servant required")