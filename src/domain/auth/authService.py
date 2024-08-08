from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,and_,or_
from ...models.userModel import User,RoleUser
from .authModel import RegisterBody,RegisterResponse,LoginBody,LoginResponse
from ...error.errorHandling import HttpException
from ...auth.createTokenUser import create_token_user
from python_random_strings import random_strings


async def Register(user : RegisterBody,session : AsyncSession) -> RegisterResponse :
    # check if user already exist with email and nomor telepon
    statementCheckCountUserByEmailOrNo_Telepon = await session.execute(select(func.count(User.id)).where(or_(User.email == user.email,User.no_telepon == user.no_telepon)))
    getCountUserByEmailOrNo_Telepon = statementCheckCountUserByEmailOrNo_Telepon.scalar_one()

    if getCountUserByEmailOrNo_Telepon  > 0 :
        raise HttpException(400,"email atau nomor telepon telah digunakan")
    
    # mapping user BaseModel and add to database 
    userMapping = user.model_dump()
    userMapping.update({"id" : str(random_strings.random_digits(6))})
    session.add(User(**userMapping))
    await session.commit()

    # create token for user
    token_payload = {"id" : userMapping["id"],"username" : userMapping["username"],"isverify" : False,"role" : None}
    token = create_token_user(token_payload)

    return {
        "msg" : "register success",
        "data" : {
            **user.model_dump(exclude={"password"}),
            "id" : userMapping["id"],
            **token
        }
    }

# async def 

