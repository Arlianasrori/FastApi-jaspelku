from fastapi import Response
from ....auth.createTokenAdmin import create_token_admin
from .authModels import LoginModel
from sqlalchemy.ext.asyncio import AsyncSession
from ....error.errorHandling import HttpException
from ....models.developerModels import Developer
from sqlalchemy import select

async def login(data : LoginModel,Session : AsyncSession,res : Response) :
    statement = await Session.execute(select(Developer).where(Developer.username == data.username))
    findAdmin = statement.scalars().first()

    if not findAdmin :
        raise HttpException(status=400,message="username or password wrong")
    
    if findAdmin.password != findAdmin.password :
        raise HttpException(status=400,message="username or password wrong")
    
    token_payload = {"sub" : findAdmin.username}

    token = create_token_admin(token_payload)
    res.set_cookie("access_token",token["access_token"])
    res.set_cookie("refresh_token",token["refresh_token"])
    return {
        "msg" : "succes",
        "data" : token
    }

def refresh_token(data,res : Response) :
    token_payload = {"sub" : data["username"]}

    token = create_token_admin(token_payload)
    res.set_cookie("access_token",token["access_token"],httponly=True,max_age="24 * 60 * 60 * 60")
    res.set_cookie("refresh_token",token["refresh_token"],httponly=True,max_age="24 * 60 * 60 * 60 * 60")
    return {
        "msg" : "succes",
        "data" : token
    }