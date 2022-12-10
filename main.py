from flask import Flask, render_template, request
import os
import serial
import random
import base64
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import threading
import time
import datetime


#definir instancia del servidor
from CodigoArduino import CodigoArduino

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/login')
def login():
    return render_template('login.html', title='App DABM')


@app.route('/validar', methods=["POST"])
def validar():
    if request.method == "POST":
        usuario = request.form['usuario']
        password = request.form['password']
    
    if usuario == "admin" and password == "escuela":
        return render_template('menu.html')
    else:
        return "<h1> Datos incorrectos</h1>"

@app.route('/registro')
def registro():
    return render_template('Registro.html',title = 'App DABM')



@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        nombre = request.form['nombre']
        password = request.form['password']

        directorio = os.path.dirname(__file__)
        archivo = 'database/users.csv'
        ruta = os.path.join(directorio,archivo)
        f = open(ruta,'a')
        f.write(nombre+';'+password)
    return render_template('login.html',title = 'App DABM')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route("/datos", methods=["GET"])
def monitor():
    print("ingresa a datos")
    sensor = CodigoArduino( "COM8")
    datos=sensor.lectura()

    return render_template('datos.html',titulo="Datos del sensor",regitros= datos)
""""
@app.route('/grafica')
def grafica():

    #plt.style.use('_mpl-gallery')

    # make data:
    #np.random.seed(3)
    x = datos
    y =

    # plot
    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    directorio = os.path.dirname(__file__)
    archivo = 'static/ejemplografica.png'
    ruta = os.path.join(directorio,archivo)

    plt.savefig(ruta)

    return render_template('plot.html')

"""
"""""
@app.route('/grafica2')
def grafica2():

    fig = Figure()
    ax = fig.subplots()
    ax.plot([1,2])

    buf = BytesIO()
    fig.savefig(buf,format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64, {data}'/>"
"""
def read_csv():
    basedir=os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'csv/users.csv')
    with open(data_file,'r') as f:
        csv_reader = csv.reader(f)
        lines=[]
        for line in csv_reader:
            lines.append(line)

    return lines

def getDatos():
    directorio = os.path.dirname(__file__)
    archivo = 'database/users.csv'
    ruta = os.path.join(directorio,archivo)
    f = open(ruta, 'r')
    lineas = f.readlines()
    f.close()

    datos=[]
    for l in lineas:
        l=l.replace("\n", "")
        l=l.split(";")
        datos.append(l)

    return datos

# punto inicial de apliacaion
if __name__ == "__main__":
    #deplegamos el servidor -> 127.0.0.1-> DNS (Traduce esa ip a url -> localhost)
    app.run(port=8082,debug=True)
