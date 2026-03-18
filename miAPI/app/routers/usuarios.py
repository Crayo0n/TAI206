from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD Usuarios"]
)

@router.get("/")
async def consultaUsuarios():
    return {
        "status": "200",
        "total":len(usuarios),
        "data": usuarios
    }
    
@router.post("/")
async def agregar_Usuario(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"]==usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "datos":usuario,
        "status": "200"
    }

@router.put("/{id}", status_code=status.HTTP_200_OK)
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
    
@router.delete("/{id}")
async def eliminar_Usuario(id:int, usuarioAuth: str = Depends(verificar_Peticion)):
    for i, usr in enumerate(usuarios):
        if usr["id"]==id:
            usuarios.pop(i)
            return{
                "mensaje":f"Usuario Eliminado correctamente por {usuarioAuth}",
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )