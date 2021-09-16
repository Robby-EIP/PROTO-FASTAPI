from typing import Optional

from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post('/push/rawcode')
def get_rawcode(test: TestItem):
    print('salut')
    print('test == ', test)
    print('test.code == ', test.code)
    return {'success': 'true'}

@app.post('/push/filecode')
def get_rawcode(test: Request):
    print('salut')
    print('test == ', test)

@app.post('/push/image')
async def image(image: UploadFile = File(...)):
    return {"filename": image.filename}