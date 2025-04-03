# blueprints/pedidos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from mi_app.database import get_db_connection  # ✅ Importa correctamente desde el paquete `mi_app`

import pandas as pd

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos') # http://127.0.0.1:5000/pedidos/crear
#CRUD de cualquier tabla 

@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    conn = get_db_connection()
    if conn:
        df_pedidos = pd.read_sql("SELECT * FROM pedidos", conn)
        conn.close()
        pedidos = df_pedidos.to_dict(orient='records')
        return render_template('pedidos/lista_pedidos.html', pedidos=pedidos)
    else:
        flash("No se pudo conectar a la base de datos", 'error')
        return redirect(url_for('pedidos.get_pedidos'))

@pedidos_bp.route('/crear', methods=['GET', 'POST'])
def crear_pedido():
    conn = get_db_connection()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descripcion = request.form['descripcion']
        monto = request.form['monto']

        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente_id, descripcion, monto) VALUES (%s, %s, %s)", 
                       (cliente_id, descripcion, monto))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Pedido creado exitosamente', 'success')
        return redirect(url_for('pedidos.get_pedidos'))
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT cliente_id, nombre FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pedidos.crear_pedido', clientes=clientes)
