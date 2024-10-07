from flask import Flask, render_template, request, jsonify, make_response
import pusher
import mysql.connector

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Cursos, Nombre_Curso, Telefono FROM tst0_cursos ORDER BY Id_Cursos DESC LIMIT 10 OFFSET 0")
    registros = cursor.fetchall()
    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id = request.form.get("id")
    Nombre_Curso = request.form["Nombre_Curso"]
    Telefono = request.form["Telefono"]

    cursor = con.cursor()
    if id:
        sql = "UPDATE tst0_cursos SET Nombre_Curso = %s, Telefono = %s WHERE Id_Cursos = %s"
        val = (Nombre_Curso, Telefono, id)
    else:
        sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
        val = (Nombre_Curso, Telefono)

    cursor.execute(sql, val)
    con.commit()
    
    notificarActualizacionCursos()
    
    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Cursos, Nombre_Curso, Telefono FROM tst0_cursos WHERE Id_Cursos = %s", (id,))
    registros = cursor.fetchall()
    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]
    cursor = con.cursor()
    cursor.execute("DELETE FROM tst0_cursos WHERE Id_Cursos = %s", (id,))
    con.commit()

    notificarActualizacionCursos()

    return make_response(jsonify({}))

def notificarActualizacionCursos():
    pusher_client = pusher.Pusher(
        app_id="1872172",
        key="ab077c6305428af0579b",
        secret="a2f133d9ea7bb1f9e37e",
        cluster="mt1",
        ssl=True
    )
    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", {})

if __name__ == "__main__":
    app.run(debug=True)
