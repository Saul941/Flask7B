# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

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

@app.route("/alumnos")
def alumnos():
    con.close()

    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código usado en las prácticas
def notificarActualizacionCursos():
    pusher_client = pusher.Pusher(
        app_id = "1872172",
        key = "ab077c6305428af0579b",
        secret = "a2f133d9ea7bb1f9e37e",
        cluster = "mt1",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", args)

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Cursos, Nombre_Curso, Telefono AS Hora FROM tst0_cursos
    ORDER BY Id_Curso DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    Nombre_Curso = request.form["Nombre_Curso"]
    Telefono     = request.form["Telefono"]
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_cursos SET
        Nombre_Curso = %s,
        Telefono     = %s
        WHERE Id_Curso = %s
        """
        val = (Nombre_Curso, Telefono, id)
    else:
        sql = """
        INSERT INTO tst0_cursos (Nombre_Curso, Telefono)
                        VALUES (%s,          %s)
        """
        val =                  (Nombre_Curso, Telefono)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionCursos()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Curso, Nombre_Curso, Telefono FROM tst0_cursos
    WHERE Id_Curso = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_cursos
    WHERE Id_Curso = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionCursos()

    return make_response(jsonify({}))
