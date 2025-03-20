from flask import Flask, jsonify, request, render_template, redirect, url_for
import mysql.connector
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

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

# Rutas CRUD (igual que antes)
# ... (get_clientes, get_cliente, mostrar_crear_cliente, create_cliente, mostrar_editar_cliente, update_cliente, delete_cliente)

# Ruta para mostrar métricas y gráficos
@app.route('/metricas')
def metricas():
    # Ejemplo de métrica: Número de clientes
    num_clientes = query_to_dataframe("SELECT COUNT(*) as num_clientes FROM clientes").iloc[0]['num_clientes']

    # Ejemplo de gráfico: Número de pedidos por cliente
    df_pedidos = query_to_dataframe("SELECT cliente_id, COUNT(*) as num_pedidos FROM pedidos GROUP BY cliente_id")
    plt.figure(figsize=(8, 6))
    sns.barplot(x='cliente_id', y='num_pedidos', data=df_pedidos)
    plt.title('Número de Pedidos por Cliente')
    plt.xlabel('ID del Cliente')
    plt.ylabel('Número de Pedidos')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('metricas.html', num_clientes=num_clientes, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)