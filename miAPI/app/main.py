#importaciones
#uvicorn main:app --reload

from fastapi import FastAPI
import asyncio
from typing import Optional

#Inicialización de la aplicación
app = FastAPI(
    title='Mi primer API',
    description='Mauricio Rodriguez Molina',
    version='1.0'
)

usuarios=[
    {"id":1,"nombre":"Mauricio","edad":20},
    {"id":2,"nombre":"Dulce","edad":20},
    {"id":3,"nombre":"Saul","edad":19}
]

#Endpoints
@app.get("/", tags=['Inicio'])
async def hola_mundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API rest con FastAPI"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje": "Tu calificación en TAI es 10"}

@app.get("/v1/usuarios/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado": id}

@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOP(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"usuario encontrado": id, 
                        "Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono ID"}
    
