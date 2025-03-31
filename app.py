from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://datos2_user:GTQMbS1hBVO0fDlZmTS9tsG1fJuJodGW@dpg-cvlflujuibrs73f12ujg-a.oregon-postgres.render.com:5432/datos2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# Ruta principal
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# Agregar
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio)
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', accion='Agregar')

# Editar
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = float(request.form['precio'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', producto=producto, accion='Editar')

# Eliminar
@app.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
