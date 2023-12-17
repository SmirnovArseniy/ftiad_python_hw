from fastapi import FastAPI, HTTPException, Body
import uvicorn
from calc import Calc

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/calculation")
def calculation(body: str = Body(...)):
    calc = Calc(body).evaluation()
    if type(calc) == float:
        return calc
    else:
        return HTTPException(400, detail=calc)


if name == "main":
    uvicorn.run(app, host="0.0.0.0", port=3003)
