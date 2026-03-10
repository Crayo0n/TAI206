from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date,datetime

from miAPI.app.main import UsuarioBase

#Inicialización de la aplicación
app = FastAPI(
    title='API Sistemas de Citas Medicas',
    description='Mauricio Rodriguez Molina',
    version='1.0'
)

fecha_actual = datetime.now()


#Modelo de validacion Pydantic
class Citas(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de cita")
    paciente: str = Field(..., min_length=5, description="Nombre del paciente")
    fecha: int = Field(..., le=fecha_actual)
    motivo: str = Field(..., max_length=100)
    confirmacion: bool = Field(..., default= 0)
    
    
    
class Pacientes(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de paciente")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=121, description="Edad valida entre 0 y 121")
    numero_citas: int 
    
citas=[]
    
    
    
#Seguridad con HTTP Basic
security = HTTPBasic()
def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "root")
    contraAuth = secrets.compare_digest(credentials.password, "1234")
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username
    

#Consultar citas
@app.get("/v1/citas/", tags=['CRUD Citas'])
async def consultaCitas(usuarioAuth: str = Depends(verificar_Peticion)):
    return {
        "status": "200",
        "total":len(citas),
        "data": citas
    }
    
#Crear Citas    
@app.post("/v1/citas/", tags=['CRUD Citas'])
async def agregar_Cita(cita:Citas, paciente:Pacientes):
    for ci in Citas:
        if ci["id"]==cita.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    for pa in Pacientes:
        if pa["numero_citas"]>3 and ci["fecha"]==cita.fecha:
            raise HTTPException(
                status_code=400,
                detail="El paciente tiene mas de 3 citas en la misma fecha"
            )
            
    Citas.append(cita)
    return{
        "mensaje":"Cita Agregado",
        "datos":cita,
        "status": "200"
    }

#Consultar Cita por ID
@app.get("/v1/citas/{id}", tags=['CRUD Citas'])
async def consultar_Cita(id:int):
    for cita in citas:
        if cita["id"]==id:
            return cita
    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )
    raise HTTPException(status_code=404, detail="Libro no encontrado en la biblioteca")


#Confirmar Citas



#Eliminar Citas
@app.delete("/v1/citas/{id}", tags=['CRUD Citas'])
async def eliminar_Cita(id:int, usuarioAuth: str = Depends(verificar_Peticion)):
    for i, usr in enumerate(citas):
        if usr["id"]==id:
            citas.pop(i)
            return{
                "mensaje":f"Cita Eliminado correctamente por {usuarioAuth}",
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Cita no encontrado"
    )