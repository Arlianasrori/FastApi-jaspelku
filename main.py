import asyncio
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
load_dotenv("/.env")

from src.socket.socket import socket_app,connetDisconnectSocket,cleanup
from src.error.errorHandling import add_exception_server
from src.routes.authRouter import authRouter
from src.routes.adminRouter import adminRouter
from src.routes.servantRouter import servantRouter
from src.routes.vendeeRouter import vendeeRouter
from src.routes.userRouter import userRouter
from src.routes.chatRouter import chatRouter

from contextlib import asynccontextmanager

# handle fastApi on event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kode inisialisasi (jika ada)
    yield
    # Kode pembersihan
    await cleanup()

App = FastAPI(title="API SPEC FOR JASPELKU PROJECT",description="This is the api spec for jaspelku, it can be your guide in consuming the api. Please pay attention to the required fields in the api spec ini",servers=[{"url": "http://localhost:2008","description" : "development server"}],contact={"name" : "Habil Arlian Asrori","email" : "arlianasrori@gmail.com"},lifespan=lifespan)


routes = [authRouter,adminRouter,servantRouter,vendeeRouter,userRouter,chatRouter]
for router in routes :
    App.include_router(router)

origins = [
    "http://localhost:2008",
]

App.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

App.mount("/foto_profile_user",StaticFiles(directory="src/public/user_foto_profile"),name="static")
App.mount("/",app=socket_app)

add_exception_server(App)
connetDisconnectSocket()

async def runServer() :
    uvicorn.run(app="main:App",port=2008,reload=True)


if __name__ == "__main__" :
    asyncio.run(runServer())