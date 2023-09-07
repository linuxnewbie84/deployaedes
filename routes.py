from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from uuid import uuid4
from trataima import img, imgw
from pydantic import BaseModel, ValidationError

class f(BaseModel):
    file = File    

rute = "imagenesr/"

router = APIRouter()
@router.get("/", tags=["Bienvenida"])
async def home():
    return HTMLResponse("<h1>Bienvenido Ovitraap</h1>")

@router.post("/subir", tags=["Subida de Archivos"])
async def upload_huevos(file:UploadFile =File(...)) -> f:
    if file.content_type == "image/jpeg":
        recibido = await file.read()
        file.filename = f"{uuid4()}.jpg"
        with open(f"{rute}{file.filename}", "wb") as huevesillor:
            huevesillor.write(recibido)
            huevesillor.close()
            l = img(rute + file.filename)
            l2 = imgw(rute+ file.filename)   
        return  l.trar()
    else:
        return HTMLResponse(f"<h1> Tu archivo es un {file.content_type}, y se necesitan archivos de imagen/h1>")
    #Se termina el tratamiento de imagenes y se guardan
   
   