from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse
import time

app = FastAPI()


@app.get("/ping")
def ping():
    time.sleep(0.02)
    return {"status":"ok"}



@app.get("/download")
def download():
    size = 5 * 1024 * 1024
    data = b"x" * size
    return data

    
@app.post("/upload")
async def upload(request: Request):
    data = await request.body()
    return {"received_bytes":(len(data))}

@app.get("/")
def root():
    return{"message":"speed test server Running"}