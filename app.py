from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Curso {self.nombre}>'

# Crear la base de datos (ejecutar solo la primera vez)
# db.create_all()

# Ruta para obtener todos los cursos o buscar por nombre
@app.route('/buscar', methods=['GET'])
def buscar_cursos():
    query = request.args.get('q', '')
    cursos = Curso.query.filter(Curso.nombre.ilike(f"%{query}%")).all()
    return jsonify([{
        'ID_Curso': curso.id,
        'Nombre_Curso': curso.nombre,
        'Telefono': curso.telefono
    } for curso in cursos])

# Ruta para agregar un curso
@app.route('/curso', methods=['POST'])
def agregar_curso():
    nombre_curso = request.form['nombre_curso']
    telefono = request.form['telefono']
    nuevo_curso = Curso(nombre=nombre_curso, telefono=telefono)
    db.session.add(nuevo_curso)
    db.session.commit()
    return jsonify({'message': 'Curso agregado'}), 200

# Ruta para obtener un curso por su ID
@app.route('/curso/<int:id>', methods=['GET'])
def get_curso(id):
    curso = Curso.query.get(id)
    if curso:
        return jsonify({
            'ID_Curso': curso.id,
            'Nombre_Curso': curso.nombre,
            'Telefono': curso.telefono
        })
    return jsonify({'message': 'Curso no encontrado'}), 404

# Ruta para actualizar un curso por su ID
@app.route('/curso/<int:id>', methods=['PUT'])
def actualizar_curso(id):
    curso = Curso.query.get(id)
    if curso:
        data = request.form
        curso.nombre = data['nombre_curso']
        curso.telefono = data['telefono']
        db.session.commit()
        return jsonify({'message': 'Curso actualizado'})
    return jsonify({'message': 'Curso no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
