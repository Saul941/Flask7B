from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id = "1872172",
    key = "ab077c6305428af0579b",
    secret = "a2f133d9ea7bb1f9e37e",
    cluster = "mt1",
    ssl=True
)

def get_db_connection():
    con = mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )
    return con

@app.route("/")
def index():
    return render_template("curso.html")

# Ruta para manejar la creación y edición de cursos
@app.route("/curso", methods=["GET", "POST"])
def curso():
    if request.method == "POST":
        id_curso = request.form.get("id_curso")
        nombre_curso = request.form["nombre_curso"]
        telefono = request.form["telefono"]

        con = get_db_connection()
        cursor = con.cursor()

        if id_curso:
            sql = """
            UPDATE tst0_cursos
            SET Nombre_Curso = %s, Telefono = %s
            WHERE ID_Curso = %s
            """
            val = (nombre_curso, telefono, id_curso)
            cursor.execute(sql, val)
        else:
            sql = "INSERT INTO tst0_cursos (Nombre_Curso, Telefono) VALUES (%s, %s)"
            val = (nombre_curso, telefono)
            cursor.execute(sql, val)

        con.commit()
        con.close()

        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
            "nombre_curso": nombre_curso,
            "telefono": telefono,
            "id_curso": id_curso if id_curso else cursor.lastrowid
        })

    return render_template("curso.html")

@app.route("/buscar")
def buscar():
    con = get_db_connection()
    cursor = con.cursor()
    search_query = request.args.get("q", "")
    if search_query:
        cursor.execute("SELECT * FROM tst0_cursos WHERE Nombre_Curso LIKE %s ORDER BY ID_Curso DESC", (f"%{search_query}%",))
    else:
        cursor.execute("SELECT * FROM tst0_cursos ORDER BY ID_Curso DESC")
    
    registros = cursor.fetchall()
    con.close()

    registros_list = [{"ID_Curso": r[0], "Nombre_Curso": r[1], "Telefono": r[2]} for r in registros]
    return jsonify(registros_list)

@app.route("/eliminar_curso", methods=["POST"])
def eliminar_curso():
    con = get_db_connection()
    if not con.is_connected():
        con.reconnect()

    id_curso = request.form["id"]

    cursor = con.cursor()
    sql = "DELETE FROM tst0_cursos WHERE ID_Curso = %s"
    val = (id_curso,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusher_client.trigger("registrosTiempoReal", "registroEliminado", {"id": id_curso})

    return jsonify({"message": "Curso eliminado correctamente"})

@app.route("/obtener_curso", methods=["GET"])
def obtener_curso():
    id_curso = request.args.get("id")
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    
    sql = "SELECT * FROM tst0_cursos WHERE ID_Curso = %s"
    cursor.execute(sql, (id_curso,))
    
    curso = cursor.fetchone()
    con.close()
    
    return jsonify(curso)

if __name__ == "__main__":
    app.run(debug=True)
