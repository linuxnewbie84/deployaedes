from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from uuid import uuid4
from trataima import img, imgw
from fastapi.templating import Jinja2Templates


rute = "imagenesr/"
ruta = "resultados/"
template= Jinja2Templates(directory="templates")

router = APIRouter()
@router.get("/", tags=["Bienvenida"], response_class=HTMLResponse)
async def home(request:Request):
    return template.TemplateResponse("index.html", {"request": request})

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
        return l.trar()
    else:
        return JSONResponse(f"Tu archivo es un {file.content_type}, y solo se pueden procesar archivos de imagen extensión jpeg")
        #return JSONResponse(f"Tu archivo es un {file.content_type}, y solo se pueden procesar archivos de imagen extensión jpeg", file.content_type)
    #Se termina el tratamiento de imagenes y se guardan
@router.get("/recibir/",tags=["Visualizar"])
async def dow(file:str):
    return FileResponse(ruta+file)
