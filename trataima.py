import numpy as np
import cv2
from uuid import uuid4
from fastapi.responses import JSONResponse, FileResponse


ruta = 'resultados/'
ruta2 = 'resultadosw/'
class img:
    def __init__(self, f):
        self.f = f
        
    def trar(self):
        huevr = cv2.imread(self.f)
        #* Cargar imagen
        
        #cv2.imshow("Original", huevr)
         
        
        esca = cv2.cvtColor(huevr, cv2.COLOR_BGR2GRAY)
        
        #*Gaussiano
        
        gaus = cv2.GaussianBlur(esca, (5,5), 0)
        
        #*Mostramos
        
        #cv2.imshow("Escalas y Gauss", gaus)
        
        #*Bordes
        
        borde = cv2.Canny(gaus, 50, 125)
        
        #cv2.imshow("Bordes", borde)
        (contornos,_) = cv2.findContours(borde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        #cv2.imwrite(ruta, huevr, )
        
        print("He encontrado {} huevesillos de Aedes Aegypti".format(len(contornos)))
        
        cv2.drawContours(huevr,contornos,-1,(0,0,255), 2)
        hallazgos = "Huevesillos Encontrados: " + str(len(contornos))
        cv2.putText(huevr, hallazgos, (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7, (255,0,0),1)
        nom = f"{uuid4()}.jpg"
        cv2.imwrite(ruta+nom, huevr)
        return JSONResponse(f"La imagen ha sido procesada y guardada con el nombre: {nom} y se han encontrado *{len(contornos)}* huevesillos del Mosquito Aedes Aegyptip")        
        #return HTMLResponse("""<h1>La imagen ha sido procesada y guardada con el nombre: {},</h1> 
#<h2>Y se han encontrado *{}* huevesillos del Mosquito Aedes Aegyptip </h2>""".format(nom,len(contornos)))

#!!Aplicación del algoritmo Watershed   
class imgw :
    def __init__(self, r):
        self.r = r
    
    def wather(self):
        huevos = cv2.imread(self.r) #*lectura
        escalas = cv2.cvtColor(huevos, cv2.COLOR_BGR2GRAY) #*Binaria
        
        #*Umbral Otsu para estimar los objetos
        _, limite= cv2.threshold(escalas, 0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        #*Apertura morfologica para eliminar el ruido
        k = np.ones((3,3), np.uint8) #dimensiones
        op = cv2.morphologyEx(limite, cv2.MORPH_OPEN, k, iterations=2)#Aplicamos morfología
        
        #*Dilatamos los limites para mostrar mejor los fondos
        b =cv2.dilate(op,k,iterations=3) #Aplicacmos la dilatación
        
        #*Transfomación de distancias de primer plano
        d_t= cv2.distanceTransform(op, cv2.DIST_L2, maskSize=5)
        _, pplano = cv2.threshold(d_t,0.7*d_t.max(),255,0)
        pplano = np.uint8(pplano)
        
        #cv2.imshow("Primer", pplano)
        
        #*substraemos los contornos que no estamos seguros estén en primer plano
        nose=cv2.subtract(b,pplano)
        
        #*Marcadores
        _, marcadores= cv2.connectedComponents(pplano)
        marcadores = marcadores+1 #Sumanos los marcadores para que no se consideres una región desconocdida
        
        marcadores[nose == 255]= 0
        
        #*Aplicamos en algoritmo Watershed a nuestra imagen original
        marcadores = cv2.watershed(huevos,marcadores)
        huevos[marcadores==-1]= [0,0,255]
        cv2.imshow("Huebos",huevos)
        #nom = f"{uuid4()}.jpg"
        
        
        
        
        

