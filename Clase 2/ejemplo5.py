import csv
from flask import Flask, render_template, request

app = Flask(__name__)

def cargar_clientes(archivo_csv):
    clientes = {}
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
        # TODO newline
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            nombre = fila['nombre'].split()[0].capitalize()  # Obtener el primer nombre y capitalizarlo
            clientes[nombre] = fila
    return clientes

clientes = cargar_clientes('clientes.csv')
print(clientes)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cliente_nombre = request.form.get('cliente_nombre').capitalize()
        if cliente_nombre in clientes:
            return render_template('clientes_csv.html', data=clientes[cliente_nombre])
        else:
            return render_template('clientes_csv.html', error="Cliente no encontrado")
    return render_template('clientes_csv.html')

if __name__ == '__main__':
    app.run(debug=True)