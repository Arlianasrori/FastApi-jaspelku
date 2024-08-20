from fastapi import Request
from ...models.userModel import RoleUser
from ...error.errorHandling import HttpException
async def vendeeAuthDepends(req : Request) :
    user = req.User
    print(user)

    if user["role"] != RoleUser.vendee :
        raise HttpException(403,"forbidden,role vendee required")