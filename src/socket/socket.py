import socketio
import asyncio
from .socket_auth_middleware import auth_middleware
from .socketHearBeat import HeartbeatManager

# Inisialisasi server Socket.IO asinkron dengan berbagai konfigurasi
sio = socketio.AsyncServer(cors_allowed_origins='*', cors_credentials=False, transports=['polling', 'websocket'], async_mode='asgi', async_handlers=True)
# Membungkus server Socket.IO dalam aplikasi ASGI
socket_app = socketio.ASGIApp(sio)

# Dictionary untuk menyimpan informasi pengguna yang sedang online
online_users = {}
# Inisialisasi HeartbeatManager untuk mengelola heartbeat pengguna
heartbeat_manager = HeartbeatManager(online_users, sio)

# Variabel untuk menyimpan task heartbeat
heartbeat_task = None

def connetDisconnectSocket() :
    from ..domain.generalUser.userService import updateIsOnlineUser
    from .socketErrorHandling import socketError
    from ..db.database import SessionLocal

    @sio.on("connect")
    async def connect(sid, environ,auth):
        try :
            # Membuat sesi database baru
            session = SessionLocal()
            # Melakukan autentikasi pengguna
            auth = await auth_middleware(sid, environ,auth)
            if not auth:
                # Mengembalikan error jika autentikasi gagal
                return await socketError(401,"Unauthorized","Unauthorized",sid)

            user_id = auth["user_id"]
            print("connect")
            # Menyimpan informasi pengguna yang baru terhubung
            online_users[sid] = {
                "user_id" : user_id,
                "last_beat" : asyncio.get_event_loop().time()
            }
            # Memperbarui status online pengguna di database
            await updateIsOnlineUser(user_id, True,session)
            # Mengirim event bahwa pengguna telah online
            await sio.emit('user_online', {'user_id': user_id,"isOnline" : True})

            # Memulai heartbeat manager jika belum berjalan
            heartbeat_manager.start_if_not_running()
        finally :
            # Menutup sesi database
            await session.close()

    @sio.on("disconnect")
    async def disconnect(sid):
        try :
            # Membuat sesi database baru
            session = SessionLocal()
            print("disconnect")
            user = online_users.get(sid)
            if user :
                # Menghapus pengguna dari daftar online
                del online_users[sid]
                # Memperbarui status offline pengguna di database
                await updateIsOnlineUser(user["user_id"], False,session)
                # Mengirim event bahwa pengguna telah offline
                await sio.emit('user_offline', {'user_id': user['user_id'],"isOnline" : False})

            # Menghentikan heartbeat manager jika tidak ada pengguna online
            if not online_users:
                    await heartbeat_manager.stop()
        finally :
            # Menutup sesi database
            await session.close()

    @sio.on("heartbeat")
    async def handle_heartbeat(sid):
        try :
            # Membuat sesi database baru
            session = SessionLocal()
            if sid in online_users:
                # Memperbarui waktu heartbeat terakhir untuk pengguna
                online_users[sid].update({"last_beat" : asyncio.get_event_loop().time()})
        finally :
            # Menutup sesi database
            await session.close()

# Fungsi untuk membersihkan sumber daya saat aplikasi ditutup
async def cleanup():
    await heartbeat_manager.stop()