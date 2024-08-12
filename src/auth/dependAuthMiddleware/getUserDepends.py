from fastapi import Request

async def GetUserDepends(req : Request) :
    return req.User