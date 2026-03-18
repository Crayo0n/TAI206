#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc

#Inicialización de la aplicación
app = FastAPI(
    title='Mi primer API',
    description='Mauricio Rodriguez Molina',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)