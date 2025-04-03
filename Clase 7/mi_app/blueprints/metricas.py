# blueprints/metricas.py
from flask import Blueprint, render_template
from mi_app.database import get_db_connection  # ✅ Importa correctamente desde el paquete `mi_app`

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

metricas_bp = Blueprint('metricas', __name__, url_prefix='/metricas')

@metricas_bp.route('/pedidos_por_cliente')
def pedidos_por_cliente():
    df_pedidos = pd.read_sql("SELECT cliente_id, COUNT(*) as num_pedidos FROM pedidos GROUP BY cliente_id", get_db_connection())

    plt.figure(figsize=(7, 5))
    sns.barplot(x='cliente_id', y='num_pedidos', data=df_pedidos)
    plt.title('Número de Pedidos por Cliente')
    plt.xlabel('ID del Cliente')
    plt.ylabel('Número de Pedidos')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('metricas/pedidos_por_cliente.html', plot_url=plot_url)
