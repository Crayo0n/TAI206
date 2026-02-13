#importaciones
#uvicorn main:app --reload

from fastapi import FastAPI, status, HTTPException
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

@app.get("/v1/parametroO/{id}", tags=['Parametro Obligatorio'])
async def consultaU(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado": id}

@app.get("/v1/parametro_op/", tags=['Parametro Opcional'])
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

@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return {
        "status": "200",
        "total":len(usuarios),
        "data": usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_Usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"]==usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuarios)
    return{
        "mensaje":"Usuario Agregado",
        "datos":usuario,
        "status": "200"
    }

@app.put("/v1/editar_usuario/{id}", tags=['CRUD Usuarios'])
async def editar_Usuario(id:int, usuario:dict):
    for i, usr in enumerate(usuarios):
        if usr["id"]==usuario.get("id"):
            usuarios[i] = usuario
            return{
                "mensaje":"Usuario Editado",
                "datos":usuario,
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )
    
@app.delete("/v1/eliminar_usuario/{id}", tags=['CRUD Usuarios'])
async def eliminar_Usuario(id:int):
    for i, usr in enumerate(usuarios):
        if usr["id"]==id:
            usuarios.pop(i)
            return{
                "mensaje":"Usuario Eliminado",
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )