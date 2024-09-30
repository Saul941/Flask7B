from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

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

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT Nombre_Curso, Telefono FROM tst0_Cursos")  # Cambiado a tu tabla y campos
    registros = cursor.fetchall()
    con.close()
    return jsonify(registros)

@app.route("/registrar", methods=["POST"])
def registrar():
    nombre_curso = request.form["nombre_curso"]
    telefono = request.form["Telefono"]

    con = get_db_connection()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_Cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
    val = (nombre_curso, telefono)
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    # Envía el evento a Pusher
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {"curso": nombre_curso, "telefono": telefono})

    return jsonify({"message": "Inscripción recibida."}), 200

if __name__ == '__main__':
    app.run(debug=True)
