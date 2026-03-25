from pydantic import BaseModel, Field
from typing import Optional

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    nombre: Optional[str] = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: Optional [int] = Field(..., ge=0, le=121, description="Edad valida entre 0 y 121")
    