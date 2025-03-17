from flask import Flask, jsonify, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # ¡Reemplaza con tu contraseña!
app.config['MYSQL_DB'] = 'fernando_cortes'

# Función para establecer la conexión
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Ruta para obtener todos los clientes (READ/LIST)
@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('lista_clientes.html', clientes=clientes)
    else:
        return "No se pudo conectar a la base de datos", 500

# Ruta para obtener un cliente por ID (READ/DETAILS)
@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cliente_id = %s", (cliente_id,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()
        if cliente:
            return render_template('detalles_cliente.html', cliente=cliente)
        else:
            return "Cliente no encontrado", 404
    else:
        return "No se pudo conectar a la base de datos", 500

# Ruta para mostrar el formulario de creación de un nuevo cliente (CREATE/FORM)
@app.route('/clientes/crear', methods=['GET'])
def mostrar_crear_cliente():
    return render_template('crear_cliente.html')

# Ruta para crear un nuevo cliente (CREATE/ACTION)
@app.route('/clientes', methods=['POST'])
def create_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']

    if not nombre or not apellido or not email:
        return "Nombre, apellido y email son requeridos", 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nombre, apellido, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, email, telefono, direccion))
            conn.commit()
            cursor.close()
            conn.close()
            # return "Cliente creado exitosamente", 201 # TODO mejorar la redireccion
            return redirect(url_for('get_clientes')) # Redirige a la lista de clientes
        
        except mysql.connector.IntegrityError:
            return "El email ya está en uso", 400
    else:
        return "No se pudo conectar a la base de datos", 500

# Ruta para mostrar el formulario de edición de un cliente (UPDATE/FORM)
@app.route('/clientes/editar/<int:cliente_id>', methods=['GET'])
def mostrar_editar_cliente(cliente_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cliente_id = %s", (cliente_id,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()
        if cliente:
            return render_template('editar_cliente.html', cliente=cliente)
        else:
            return "Cliente no encontrado", 404
    else:
        return "No se pudo conectar a la base de datos", 500

# Ruta para actualizar un cliente (UPDATE/ACTION)
@app.route('/clientes/<int:cliente_id>', methods=['POST'])
def update_cliente(cliente_id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE clientes SET nombre = %s, apellido = %s, email = %s, telefono = %s, direccion = %s WHERE cliente_id = %s", (nombre, apellido, email, telefono, direccion, cliente_id))
            conn.commit()
            cursor.close()
            conn.close()
            # return "Cliente actualizado exitosamente" #TODO redireccionar
            return redirect(url_for('get_clientes')) # Redirige a la lista de clientes

        except mysql.connector.IntegrityError:
            return "El email ya está en uso", 400
    else:
        return "No se pudo conectar a la base de datos", 500

# Ruta para eliminar un cliente (DELETE)
@app.route('/clientes/eliminar/<int:cliente_id>', methods=['GET'])
def delete_cliente(cliente_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE cliente_id = %s", (cliente_id,))
        conn.commit()
        cursor.close()
        conn.close()
        # return "Cliente eliminado exitosamente" #TODO redireccionar
        return redirect(url_for('get_clientes')) # Redirige a la lista de clientes
    
    else:
        return "No se pudo conectar a la base de datos", 500

if __name__ == '__main__':
    app.run(debug=True)