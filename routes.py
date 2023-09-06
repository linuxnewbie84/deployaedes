from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from uuid import uuid4
from trataima import img, imgw
import os

rute = "imagenesr/"

router = APIRouter()
@router.post("/subir/", tags=["Subida de Archivos"])
async def upload_huevos(file:UploadFile =File(...)):
    file.filename = f"{uuid4()}.jpg"
    recibido = await file.read()
    with open(f"{rute}{file.filename}", "wb") as huevesillor:
        huevesillor.write(recibido)
        huevesillor.close()
        l = img(rute + file.filename)
        l2 = imgw(rute+ file.filename)   
    return l.trar()
#Se termina el tratamiento de imagenes y se guardan
   
   