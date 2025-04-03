# blueprints/clientes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from mi_app.database import get_db_connection  # ✅ Importa correctamente desde el paquete `mi_app`


clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('clientes/lista_clientes.html', clientes=clientes)
    else:
        flash("No se pudo conectar a la base de datos", 'error')
        return redirect(url_for('clientes.get_clientes'))

@clientes_bp.route('/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        if not nombre or not apellido or not email:
            flash("Nombre, apellido y email son obligatorios", 'error')
            return redirect(url_for('clientes.crear_cliente'))

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombre, apellido, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)", 
                           (nombre, apellido, email, telefono, direccion))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('clientes.get_clientes'))
        else:
            flash("No se pudo conectar a la base de datos", 'error')
    
    return render_template('clientes/crear_cliente.html')
