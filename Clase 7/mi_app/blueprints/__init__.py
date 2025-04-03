from flask import Blueprint

# Importa y registra los blueprints
from .clientes import clientes_bp
from .pedidos import pedidos_bp
from .metricas import metricas_bp

def register_blueprints(app):
    app.register_blueprint(clientes_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(metricas_bp)
