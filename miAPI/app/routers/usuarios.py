from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD Usuarios"]
)

@router.get("/")
async def consultaUsuarios(db: Session = Depends(get_db)):
    consulta_usuarios = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(consulta_usuarios),
        "data": consulta_usuarios
    }
    
@router.post("/")
async def agregar_Usuario(usuario:UsuarioBase, db: Session = Depends(get_db)):
    
    nuevoUsuario=usuarioDB(nombre=usuario.nombre, edad=usuario.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return{
        "mensaje":"Usuario Agregado",
        "datos":nuevoUsuario,
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