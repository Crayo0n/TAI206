#importaciones
from fastapi import FastAPI

#Inicialización de la aplicación
app = FastAPI()

#Endpoints
@app.get("/")
async def hola_mundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API rest con FastAPI"}