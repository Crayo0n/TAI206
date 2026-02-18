from flask import Flask, render_template, request, redirect
import requests

api_url="http://localhost:5000/v1/usuarios/"

app = Flask(__name__)

#ruta de inicio
@app.route('/')
def home():
    respuesta = requests.get(api_url)
    datos = respuesta.json()
    lista_usuarios = datos.get("data", [])
    
    return render_template("vista.html", usuarios=lista_usuarios)



#ruta de guardar
@app.route('/guardar' , methods=['POST'])
def agregar_Usuario():
    nuevo_usuario = {
        "id": request.form.get("id_usuario"),
        "nombre": request.form.get("nombre"),
        "edad": request.form.get("edad")
    }
    requests.post(api_url, json=nuevo_usuario)
    
    return redirect("/")
    
#ruta de eliminar
@app.route('/eliminar/<int:id>')
def eliminar_usuario(id):
    requests.delete(f"{api_url}{id}")
    return redirect("/")


if __name__ == '__main__':
    app.run(port=3000, debug=True)