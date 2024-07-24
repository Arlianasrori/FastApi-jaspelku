import asyncio
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from src.error.errorHandling import add_exception_server

import src.db.database as db
import src.models

from src.routes.authRouter import authRouter
from src.routes.adminRouter import adminRouter

App = FastAPI()

db.Base.metadata.create_all(bind=db.engine)

routes = [authRouter,adminRouter]
for router in routes :
    App.include_router(router)

add_exception_server(App)
async def runServer() :
    uvicorn.run(app="main:App",port=2008,reload=True)

if __name__ == "__main__" :
    asyncio.run(runServer())