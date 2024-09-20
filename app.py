from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos ORDER BY Id_Curso DESC")
    registros = cursor.fetchall()
    con.close()
    return jsonify(registros)

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    con = get_db_connection()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono, Fecha_Hora) VALUES (%s, %s, %s)"
    val = (args["Nombre_Curso"], args["Telefono"], datetime.datetime.now(pytz.timezone("America/Matamoros")))
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1868456",
        key="2a2b4a22ea18bf23113a",
        secret="62943ef022cd594bdde4",
        cluster="mt1",
        ssl=True
    )

    pusher_client.trigger("canalRegistroscursos", "registrocursos", args)
    return args

if __name__ == "__main__":
    app.run(debug=True)
