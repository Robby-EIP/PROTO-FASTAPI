from typing import Optional

from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import aiofiles
import os
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
    os.chdir('/home/chamet/delivery/PROTO-FASTAPI/assets/')
    async with aiofiles.open(f"./{file.filename}", 'wb+') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    temp = file.filename.split('.')
    if temp[len(temp) - 1] == 'hex':
        os.system('mv *.hex assets.hex')
        os.system('/home/chamet/Bureau/arduino-1.8.16/hardware/tools/avr/bin/avrdude -C/home/chamet/Bureau/arduino-1.8.16/hardware/tools/avr/etc/avrdude.conf -v -c arduino -p atmega328p -P net:172.20.10.2:80 -Uflash:w:./assets.hex:i')
        os.system('rm *.hex')
    elif temp[len(temp) - 1] == 'ino':
        os.system('mv *.ino assets.ino')
        os.system('/home/chamet/Bureau/arduino-cli board attach arduino:avr:uno')
        os.system('/home/chamet/Bureau/arduino-cli compile ./assets/ -e')
        os.system('/home/chamet/Bureau/arduino-1.8.16/hardware/tools/avr/bin/avrdude -C/home/chamet/Bureau/arduino-1.8.16/hardware/tools/avr/etc/avrdude.conf -v -c arduino -p atmega328p -P net:172.20.10.2:80 -Uflash:w:./build/arduino.avr.uno/assets.ino.hex:i')
        os.system('rm -rf build')
        os.system('rm *.ino')
        os.system('rm sketch.json')
    return {"success": "true"}