from flask import Flask
# from mi_app.database import register_blueprints
from mi_app.blueprints import register_blueprints
from mi_app.database import get_db_connection

app = Flask(__name__)

# Cargar configuración si tienes `config.py`
app.config.from_object("mi_app.config")

# Registra los blueprints
register_blueprints(app)
