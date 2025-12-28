from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

@app.get("/download")

def download_test():
    def generate():
        for _ in range(10):
            yield b"x" * 1024 *1024
            time.sleep(0.1)
        return StreamingResponse(generate(),media_type= "application/octet-stream")
    
@app.post("/upload")

def upload_test(data:bytes):
    return{
        "status" : "received",
        "size" : len(data)
    }