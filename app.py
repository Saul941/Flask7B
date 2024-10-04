from flask import Flask, render_template, request, jsonify, make_response
import pusher
import mysql.connector

app = Flask(__name__)

# Función para conectarse a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

# Ruta principal
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para mostrar alumnos
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Ruta para guardar alumnos
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Función para notificar actualizaciones de cursos usando Pusher
def notificarActualizacionCursos():
    pusher_client = pusher.Pusher(
        app_id="1872172",
        key="ab077c6305428af0579b",
        secret="a2f133d9ea7bb1f9e37e",
        cluster="mt1",
        ssl=True
    )
    pusher_client.trigger("canalRegistrosInscripcionCursos", "registroInscripcionCursos", {})

# Ruta para buscar los últimos cursos registrados
@app.route("/buscar")
def buscar():
    con = obtener_conexion()
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
        SELECT Id_Curso, Nombre_Curso, Telefono 
        FROM tst0_cursos
        ORDER BY Id_Curso DESC
        LIMIT 10 OFFSET 0
        """)
        registros = cursor.fetchall()
        return make_response(jsonify(registros))
    finally:
        con.close()

# Ruta para guardar nuevos registros de cursos
@app.route("/guardar", methods=["POST"])
def guardar():
    con = obtener_conexion()
    try:
        id_curso = request.form["id"]
        nombre_curso = request.form["curso"]
        telefono = request.form["telefono"]

        cursor = con.cursor()

        if id_curso:
            # Actualizar curso existente
            sql = """
            UPDATE tst0_cursos SET
            Nombre_Curso = %s,
            Telefono     = %s
            WHERE Id_Curso = %s
            """
            val = (nombre_curso, telefono, id_curso)
        else:
            # Insertar nuevo curso (sin Fecha_Registro)
            sql = """
            INSERT INTO tst0_cursos (Nombre_Curso, Telefono)
            VALUES (%s, %s)
            """
            val = (nombre_curso, telefono)

        cursor.execute(sql, val)
        con.commit()

        notificarActualizacionCursos()

        return make_response(jsonify({}))
    finally:
        con.close()

# Ruta para editar un curso existente
@app.route("/editar", methods=["GET"])
def editar():
    con = obtener_conexion()
    try:
        id_curso = request.args["id"]

        cursor = con.cursor(dictionary=True)
        sql = "SELECT Id_Curso, Nombre_Curso, Telefono FROM tst0_cursos WHERE Id_Curso = %s"
        val = (id_curso,)

        cursor.execute(sql, val)
        registros = cursor.fetchall()

        return make_response(jsonify(registros))
    finally:
        con.close()

# Ruta para eliminar un curso
@app.route("/eliminar", methods=["POST"])
def eliminar():
    con = obtener_conexion()
    try:
        id_curso = request.form["id"]

        cursor = con.cursor()
        sql = "DELETE FROM tst0_cursos WHERE Id_Curso = %s"
        val = (id_curso,)

        cursor.execute(sql, val)
        con.commit()

        notificarActualizacionCursos()

        return make_response(jsonify({}))
    finally:
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
