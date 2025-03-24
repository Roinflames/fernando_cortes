from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import mysql.connector
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__, static_folder='./styles')

# Configuración de la conexión MySQL (igual que antes)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # ¡Reemplaza con tu contraseña!
app.config['MYSQL_DB'] = 'fernando_cortes'

# Función para establecer la conexión (igual que antes)
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

# Función para convertir consultas SQL a DataFrames de Pandas
def query_to_dataframe(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Nueva ruta para redirigir desde la raíz a /clientes
@app.route('/')
def root():
    return redirect(url_for('get_clientes'))

# Rutas CRUD (igual que antes)
# Ruta para obtener todos los clientes (READ/LIST)
@app.route('/clientes', methods=['GET'])
def get_clientes():
    print("get_clientes")
    conn = get_db_connection()
    print("esta es", conn)
    print(conn is None)
    if conn is None:
        try:
            return render_template('error_db.html', message="No se pudo conectar a la base de datos. Por favor, verifica el servicio MySQL."), 500
        except Exception as e:
            print(f"Error al renderizar error_db.html: {e}")
            return "Ocurrió un error al mostrar la página de error.", 500
        
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
            flash('Cliente creado exitosamente', 'success')  # Agrega un mensaje flash
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
            flash('Cliente actualizado exitosamente', 'success')
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
        flash('Cliente eliminado exitosamente', 'success')
        return redirect(url_for('get_clientes')) # Redirige a la lista de clientes
    
    else:
        return "No se pudo conectar a la base de datos", 500

@app.route('/metricas')
def metricas_index():
    return render_template('metricas_index.html')

# Obtener todos los pedidos
@app.route('/pedidos')
def get_pedidos():
    pedidos = query_to_dataframe("SELECT * FROM pedidos").to_dict(orient='records')
    return render_template('pedidos.html', pedidos=pedidos)

# Ruta para mostrar métricas y gráficos
@app.route('/metricas/pedidos_por_cliente')
def pedidos_por_cliente():
    # Ejemplo de métrica: Número de Pedidos por Cliente
    # iloc es un indexador basado en enteros en Pandas, que se utiliza para seleccionar filas y columnas por su posición.
    num_clientes = query_to_dataframe("SELECT COUNT(*) as num_clientes FROM clientes").iloc[0]['num_clientes']

    # Ejemplo de gráfico: Número de pedidos por cliente
    df_pedidos = query_to_dataframe("SELECT cliente_id, COUNT(*) as num_pedidos FROM pedidos GROUP BY cliente_id")
    # plt.figure crea una nueva figura de matplotlib con un tamaño de 8x6 pulgadas.
    plt.figure(figsize=(8, 6))
    # sns.barplot es una función de Seaborn que se utiliza para crear gráficos de barras.
    sns.barplot(x='cliente_id', y='num_pedidos', data=df_pedidos)
    plt.title('Número de Pedidos por Cliente')
    plt.xlabel('ID del Cliente')
    plt.ylabel('Número de Pedidos')
    # img = BytesIO() se utiliza para crear un búfer en memoria donde se guardará la imagen generada por matplotlib. 
    img = BytesIO()
    # plt.savefig guarda la imagen en el búfer img en formato PNG.
    plt.savefig(img, format='png')
    # img.seek(0) se utiliza para mover el cursor al inicio del búfer.
    img.seek(0)
    # base64.b64encode(img.getvalue()) se utiliza para convertir la imagen en un string codificado en base64.
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # render_template renderiza la plantilla pedidos_por_cliente.html y pasa las variables num_clientes y plot_url a la plantilla.
    return render_template('pedidos_por_cliente.html', num_clientes=num_clientes, plot_url=plot_url)

@app.route('/metricas/monto_total_pedidos')
def monto_total_pedidos():
    # Calcular el monto total de pedidos
    monto_total = query_to_dataframe("SELECT SUM(monto) as monto_total FROM pedidos").iloc[0]['monto_total']
    return render_template('monto_total_pedidos.html', monto_total=monto_total)

if __name__ == '__main__':
    app.run(debug=True)