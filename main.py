'''
Created By : Christian Merriman
Date : 2/2026

Purpose : To architect a scalable client-server interface that bridges a Python-based backend with a responsive web frontend, enabling secure, 
low-latency communication with a locally hosted Large Language Model (LLM).

Files needed : 
main.py (this file)
model_used.py
SentinalAI.py
index.html
styles.css
script.js

'''
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import psutil
import time

# Your custom classes
from model_used import Ask_Model
from SentinalAI import SentinelAI

app = FastAPI()

# 1. ALLOW CORS: This is critical so your browser can talk to your local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_handler = SentinelAI()
model_engine = Ask_Model()
start_time = time.time()

class ChatSession(BaseModel):
    messages: List[dict]

# --- ENDPOINT: Fetch history on Page Load ---
@app.get("/get_history")
async def get_history():
    history = ai_handler.load_chat()
    # Ensure it returns an empty list if no file exists yet
    return {"history": history if history else []}

# --- ENDPOINT: System Stats ---
@app.get("/stats")
async def get_stats():
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "net_down": psutil.net_io_counters().bytes_recv / 1024 / 1024, # MB
        "net_up": psutil.net_io_counters().bytes_sent / 1024 / 1024, # MB
        "processes": len(psutil.pids()),
        "uptime": time.time() - start_time
    }

# --- ENDPOINT: The Chat Logic ---
@app.post("/ask_sentinel")
async def ask_sentinel(session: ChatSession):
    history = session.messages
    
    # Extract the last message as the current prompt
    user_prompt = history[-1]['content']
    
    # Remove it temporarily because your class function appends it again
    history.pop()

    sys_info = "You are a tactical terminal for a BAE engineer."

    # Call your Ask_Model class
    reply, updated_history = model_engine.ask_model_with_chat_history(
        prompt=user_prompt, 
        chat_history=history, 
        system_instructions=sys_info
    )

    # Save the history to the JSON file via SentinelAI class
    ai_handler.save_chat(updated_history)

    return {"reply": reply, "history": updated_history}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)