from fastapi import FastAPI
from src import route

app = FastAPI(title="Servidor WebSocket")

app.include_router(route)

# class ConnectionManager:
#     """Gestiona las conexiones activas y el broadcast de mensajes."""
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         print("conectando...")
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# manager = ConnectionManager()

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     """
#     Cada cliente se conecta a ws://<host>:<puerto>/ws
#     Todo lo que envíe un cliente se retransmite a todos (eco/broadcast).
#     """
#     await manager.connect(websocket)
#     try:
#         await manager.send_personal_message("👋 Conexión establecida.", websocket)
#         while True:
#             data = await websocket.receive_text()
#             print(data);
#             await manager.broadcast(f"🔈 {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast("❌ Un usuario se ha desconectado.")
