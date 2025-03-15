import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def cargar_clientes(archivo_csv):
    clientes = {}
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            nombre = fila['nombre'].split()[0].capitalize()
            clientes[nombre] = fila
    return clientes

def guardar_clientes(archivo_csv, clientes):
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
        campos = ['nombre', 'edad', 'ciudad']
        escritor_csv = csv.DictWriter(archivo, fieldnames=campos)
        escritor_csv.writeheader()
        for cliente in clientes.values():
            escritor_csv.writerow(cliente)

clientes = cargar_clientes('clientes.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cliente_nombre = request.form.get('cliente_nombre').capitalize()
        if cliente_nombre in clientes:
            return redirect(url_for('editar', cliente_nombre=cliente_nombre))
        else:
            return render_template('clientes.html', error="Cliente no encontrado")
    return render_template('clientes.html')

@app.route('/editar/<cliente_nombre>', methods=['GET', 'POST'])
def editar(cliente_nombre):
    if request.method == 'POST':
        clientes[cliente_nombre]['nombre'] = request.form['nombre']
        clientes[cliente_nombre]['edad'] = request.form['edad']
        clientes[cliente_nombre]['ciudad'] = request.form['ciudad']
        guardar_clientes('clientes.csv', clientes)
        return redirect(url_for('index'))
    return render_template('editar.html', cliente=clientes[cliente_nombre])

if __name__ == '__main__':
    app.run(debug=True)