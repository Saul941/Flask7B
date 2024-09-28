from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

# Configura la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

# Configura Pusher
pusher_client = pusher.Pusher(
    app_id="1714541",
    key="2df86616075904231311",
    secret="2f91d936fd43d8e85a1a",
    cluster="us2",
    ssl=True
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnos_guardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT ID_Curso, Nombre_Curso FROM tst0_cursos")  # Cambiado a tu tabla y campos
    registros = cursor.fetchall()
    con.close()

    # Convierte los registros a un formato JSON
    return jsonify(registros)

@app.route("/inscribir", methods=["POST"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    sql = "INSERT INTO tst0_Cursos (Nombre_Curso, Telefono ) VALUES (%s, %s)"
    val = (args["nombre_curso"], args["Telefono"])
    cursor.execute(sql, val)
    
    con.commit()
    con.close()
    
  

    # Envía el evento a Pusher
    pusher_client.trigger("canalRegistrosCursos", "nuevoCurso", {"curso_id": curso_id, "telefono": telefono})

    return jsonify({"message": "Inscripción recibida."}), 200

if __name__ == '__main__':
    app.run(debug=True)
