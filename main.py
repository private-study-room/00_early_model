from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# FastAPI: 비동기 웹 프레임워크로, API를 쉽게 구축할 수 있게 해줍니다.
# WebSocket: 실시간 통신을 위한 프로토콜로, 클라이언트와 서버 간의 양방향 통신을 지원합니다.

from fastapi.responses import HTMLResponse # HTML 페이지를 반환하는 데 사용
from typing import List,Dict

app = FastAPI()

# 채팅 룸을 관리할 딕셔너리 (room_id -> WebSocket list)
chat_rooms: Dict[str, List[WebSocket]] = {}

responses = {
    "안녕하세요": "안녕하세요! 무엇을 도와드릴까요?",
    "이름이 뭐예요?": "저는 규칙 기반 챗봇입니다.",
    "날씨가 어때요?": "오늘 날씨는 맑습니다.",
    "종료": "챗봇을 종료합니다."
}

# HTML 페이지를 반환하는 엔드포인트
@app.get("/")
async def get():
    return HTMLResponse("""
    <html>
        <head>
            <title>WebSocket Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <label for="room">Room ID: </label>
            <input id="roomInput" type="text" placeholder="Enter room ID"/>
            <br/>
            <input id="messageInput" type="text" placeholder="Type a message..."/>
            <button id="sendButton">Send</button>
            <ul id="messages"></ul>
            <script>
                let socket;
                const messages = document.getElementById("messages");
                const sendButton = document.getElementById("sendButton");
                const messageInput = document.getElementById("messageInput");
                const roomInput = document.getElementById("roomInput");

                // 방에 연결
                sendButton.onclick = function() {
                    if (!socket) {
                        const roomId = roomInput.value;
                        socket = new WebSocket("ws://localhost:8000/ws/" + roomId);
                        
                        socket.onmessage = function(event) {
                            const message = document.createElement("li");
                            message.textContent = event.data;
                            messages.appendChild(message);
                        };
                    }

                    const message = messageInput.value;
                    socket.send(message);
                    messageInput.value = '';
                };
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws/{room_id}")
async def chatbot(websocket: WebSocket, room_id : str):
    # 방이 없는 경우 리스트를 생성함
    if room_id not in chat_rooms:
        chat_rooms[room_id] = []

    chat_rooms[room_id].append(websocket)
    # 웹소켓 수락 및 메세지 수신
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            if data in responses:
                reply = responses[data]
            else:
                reply = "답변이 불가능합니다."
        
            for client in chat_rooms[room_id]:
                await client.send_text(f"Client : {data}")
                await client.send_text(f"chatbot:{reply}")

            if data == "종료" :
                await websocket.close()
                break
            
    except WebSocketDisconnect:
        chat_rooms[room_id].remove(websocket)
        if not chat_rooms[room_id]:
            del chat_rooms[room_id]

# pip install fastapi uvicorn[standard] FastAPI, WebSocket, WebSocketDisconnect
# uvicorn main:app --reload