from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class SumData(BaseModel):
    a: float
    b: float
    c: float

@app.post("/sum")
async def sum(data: SumData):
    result = data.a + data.b + data.c
    return {"sum": result}

if __name__ == "__main__":
    uvicorn.run("practice:app", host="0.0.0.0", port=8000, reload=True)
