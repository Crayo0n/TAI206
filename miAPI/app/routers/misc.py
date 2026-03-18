from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Miselanea"])

#Endpoints
@router.get("/")
async def hola_mundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@router.get("/bienvenidos")
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API rest con FastAPI"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje": "Tu calificación en TAI es 10"}

@router.get("/v1/parametroO/{id}")
async def consultaU(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado": id}

@router.get("/v1/parametro_op/")
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

