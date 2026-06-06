from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ESP Message Server")

message_store = {
    "id": 0,
    "text": "",
    "created_at": None,
}


class MessageIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "esp-message-server",
        "endpoints": ["/send", "/message", "/docs"],
    }


@app.post("/send")
def send_message(message: MessageIn):
    text = message.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")

    message_store["id"] += 1
    message_store["text"] = text
    message_store["created_at"] = datetime.now(timezone.utc).isoformat()

    return {
        "ok": True,
        "message": message_store,
    }


@app.get("/message")
def get_message():
    return {
        "ok": True,
        "message": message_store,
    }


@app.post("/clear")
def clear_message():
    message_store["id"] += 1
    message_store["text"] = ""
    message_store["created_at"] = datetime.now(timezone.utc).isoformat()

    return {
        "ok": True,
        "message": message_store,
    }