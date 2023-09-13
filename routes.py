from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from uuid import uuid4
from trataima import img, imgw


rute = "imagenesr/"
ruta = "resultados/"

router = APIRouter()
@router.get("/", tags=["Bienvenida"])
async def home():
    return JSONResponse({"home":"Bienvenidos"})

@router.post("/subir", tags=["Subida de Archivos"])
async def upload_huevos(file:UploadFile =File(...)):
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
        return JSONResponse(f"Tu archivo es un {file.content_type}, y solo se pueden procesar archivos de imagen")
    #Se termina el tratamiento de imagenes y se guardan
@router.get("/recibir/{file}",tags=["Descargas"])
async def dow(file:str):
    return FileResponse(ruta+file)
