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

#Consulta todos Usuarios
@router.get("/")
async def consultaUsuarios(db: Session = Depends(get_db)):
    consulta_usuarios = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(consulta_usuarios),
        "data": consulta_usuarios
    }

#Consulta un usuario
@router.get("/{id}")
async def consultaUsuario_ID(id: int, db: Session = Depends(get_db)):
    usuario_ID = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    return {
        "status": "200",
        "data": usuario_ID
    }   

#Agregar un usuario
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

#Editar Usuario
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def editar_Usuario(id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_existente = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    usuario_existente.nombre = usuario.nombre
    usuario_existente.edad = usuario.edad
    db.commit()
    db.refresh(usuario_existente)
    return {
        "mensaje": "Usuario Editado",
        "datos": usuario_existente
    }


#Editar Usuario (Patch)
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def editarU_patch(id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    editaUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    if usuario.nombre is not None:
        editaUsuario.nombre = usuario.nombre
    if usuario.edad is not None:
        editaUsuario.edad = usuario.edad
    
    db.commit()
    db.refresh(editaUsuario)
    
    return {
        "mensaje": "Usuario Editado",
        "datos": editaUsuario,
        "status": "200"
    }

#Eliminar Usuario
@router.delete("/{id}")
async def eliminar_Usuario(id:int, db: Session= Depends(get_db), usuarioAuth: str = Depends(verificar_Peticion)):
    usuario_ID = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    db.delete(usuario_ID)
    db.commit()
    return {
        "mensaje": f"Usuario Eliminado correctamente por {usuarioAuth}",
        "status": "200"
    }

