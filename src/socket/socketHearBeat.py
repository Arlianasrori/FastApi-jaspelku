import asyncio
from ..domain.generalUser.userService import updateIsOnlineUser
from ..db.database import SessionLocal

session = SessionLocal()

class HeartbeatManager:
    # Interval waktu (dalam detik) antara setiap pemeriksaan heartbeat
    HEARTBEAT_INTERVAL = 25
    # Batas waktu (dalam detik) sebelum pengguna dianggap offline jika tidak ada heartbeat
    HEARTBEAT_TIMEOUT = 10

    def __init__(self, online_users, sio):
        # Dictionary untuk menyimpan informasi pengguna online
        self.online_users = online_users
        # Instance Socket.IO server
        self.sio = sio
        # Task asyncio untuk menjalankan loop heartbeat
        self.task = None

    async def heartbeat(self):
        while True:
            try:
                # Menunggu selama interval heartbeat sebelum pemeriksaan berikutnya
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)
                # Mendapatkan waktu saat ini
                current_time = asyncio.get_event_loop().time()
                # List untuk menyimpan pengguna yang akan dianggap offline
                offline_users = []
                
                # Memeriksa setiap pengguna dalam dictionary online_users
                for userItem in self.online_users.items():
                    sid, user = userItem
                    # Jika waktu sejak heartbeat terakhir melebihi batas, anggap pengguna offline
                    if current_time - user['last_beat'] > self.HEARTBEAT_INTERVAL + self.HEARTBEAT_TIMEOUT:
                        offline_users.append({"sid": sid, "user_id": user["user_id"]})

                # Memproses pengguna yang dianggap offline
                for user in offline_users:
                    # Menghapus pengguna dari dictionary online_users
                    del self.online_users[user["sid"]]
                    # Memperbarui status pengguna menjadi offline di database
                    await updateIsOnlineUser(user["user_id"], False, session)
                    # Mengirim event 'user_offline' ke semua klien
                    await self.sio.emit('user_offline', {'user_id': user["user_id"]})
            finally:
                # Memastikan sesi database ditutup setelah setiap iterasi
                await session.close()

    def start_if_not_running(self):
        # Memulai task heartbeat jika belum berjalan atau sudah selesai
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self.heartbeat())

    async def stop(self):
        # Menghentikan task heartbeat jika sedang berjalan
        if self.task and not self.task.done():
            # Membatalkan task
            self.task.cancel()
            try:
                # Menunggu task selesai dibatalkan
                await self.task
            except asyncio.CancelledError:
                # Menangani error pembatalan task
                pass
            # Mengatur task kembali ke None
            self.task = None