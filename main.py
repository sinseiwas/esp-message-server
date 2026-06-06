from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI()

last_message = {
    "id": 0,
    "text": "",
    "created_at": None,
}


class MessageIn(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "ok", "service": "esp-message-server"}


@app.post("/send")
def send_message(message: MessageIn):
    text = message.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")

    last_message["id"] += 1
    last_message["text"] = text
    last_message["created_at"] = datetime.now(timezone.utc).isoformat()

    return {
        "ok": True,
        "message": last_message,
    }


@app.get("/message")
def get_message():
    return last_message