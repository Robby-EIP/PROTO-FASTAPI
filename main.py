from typing import Optional

from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import aiofiles
# import aiofiles

testvar:int = 0

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class TestItem(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/push/rawcode')
def get_rawcode(test: TestItem):
    f = open('./assets/code' + str(testvar) + '.txt', "w")
    f.write(test.code)
    return {'success': 'true'}

@app.post('/push/image')
async def image(file: UploadFile = File(...)):
    print(file)
    async with aiofiles.open(f"./assets/{file.filename}", 'wb+') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    return {"success": "true"}