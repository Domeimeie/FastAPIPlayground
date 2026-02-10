from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class LoginData(BaseModel):
    username: str
    password: str

app = FastAPI()


@app.get("/status")
async def getStatus():
    return {"status": "ok"}

@app.post("/login")
async def login(loginData: LoginData):
    if loginData.username == "test" and loginData.password == "1234":
        return {"login": "ok"}
    return JSONResponse(status_code=401, content={"status": "error"})