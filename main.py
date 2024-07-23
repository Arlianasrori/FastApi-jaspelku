import asyncio
from fastapi import FastAPI, Request
from fastapi import Depends
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from src.error.errorHandling import add_exception_server
from fastapi import Depends
from src.auth.adminAuthCookie import adminCookieAuth

# import src.db.database as db
# import src.models
from src.routes.authRouter import authRouter
App = FastAPI()

# db.Base.metadata.create_all(bind=db.engine)

routes = [authRouter]
for router in routes :
    App.include_router(router)

add_exception_server(App)
async def runServer() :
    uvicorn.run(app="main:App",port=2008,reload=True)

if __name__ == "__main__" :
    asyncio.run(runServer())