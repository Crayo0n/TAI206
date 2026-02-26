from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime

app = FastAPI(
    title="API de Biblioteca Digital",
    description="Mauricio Rodriguez Molina",
    version="1.0"
)

class EstadoLibro(str, Enum):
    disponible = "disponible"
    prestado = "prestado"

# Modelo para el Usuario
class Usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example=1)
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")

# Modelo para el Libro
class Libro(BaseModel):
    id_libro: int = Field(..., gt=0, description="Identificador de libro", example=1)
    nombre: str = Field(..., min_length=2, max_length=100)
    anio_publicacion: int = Field(..., gt=1450, le=AÑO_ACTUAL)
    paginas: int = Field(..., gt=1)
    estado: EstadoLibro = Field(default=EstadoLibro.disponible)

class Prestamo(BaseModel):
    id_prestamo: int = Field(..., gt=0, description="Identificador de Prestamo", example=1)
    id_libro: int 
    nombre_libro: str
    correo_usuario: EmailStr
