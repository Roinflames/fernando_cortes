from flask import Flask
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

# Ejemplo de ruta que usa la conexión
@app.route('/')
def index():
    conn = get_db_connection()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")  # Reemplaza con tu consulta
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(result)  # Muestra los resultados (¡adapta esto!)
    else:
        return "No se pudo conectar a la base de datos"

if __name__ == '__main__': #TODO profundizar __main__
    app.run(debug=True)