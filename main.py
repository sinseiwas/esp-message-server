from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ESP Message Server")

messages = []
next_id = 1


class MessageIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    author: str = Field(default="Dan", max_length=50)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "esp-message-server",
        "endpoints": ["/send", "/messages", "/latest", "/clear", "/docs"],
    }


@app.post("/send")
def send_message(message: MessageIn):
    global next_id

    text = message.text.strip()
    author = message.author.strip() or "Dan"

    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")

    item = {
        "id": next_id,
        "author": author,
        "text": text,
        "type": "text",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    next_id += 1
    messages.append(item)

    if len(messages) > 50:
        messages.pop(0)

    return {"ok": True, "message": item}


@app.get("/messages")
def get_messages():
    return {"ok": True, "messages": messages}


@app.get("/latest")
def get_latest():
    if not messages:
        return {"ok": True, "message": None}
    return {"ok": True, "message": messages[-1]}


@app.post("/clear")
def clear_messages():
    messages.clear()
    return {"ok": True}