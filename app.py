from flask import Flask

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()

    return render_template("app.html")

# Ejemplo de ruta GET usando templates para mostrar una vista
@app.route("/alumnos")
def alumnos():
    con.close()

    return render_template("alumnos.html")

# Ejemplo de ruta POST para ver cómo se envia la informacion
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código usado en las prácticas
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos ORDER BY Id_Curso DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
    val = (args["curso"], args["telefono"])
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id = "1872172",
        key = "ab077c6305428af0579b",
        secret = "a2f133d9ea7bb1f9e37e",
        cluster = "mt1",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", args)

    return args
