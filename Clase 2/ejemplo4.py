from flask import Flask, render_template, request

app = Flask(__name__)

clientes = {
    'Rodrigo': {'name': 'Rodrigo Reyes', 'city': 'Santiago', 'age': 40},
    'Fernando': {'name': 'Fernando Cortés', 'age': 30, 'city': 'Santiago'},
    'Ana': {'name': 'Ana Perez', 'age': 25, 'city': 'Valparaiso'} #Agregamos un cliente para mostrar el ejemplo
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cliente_nombre = request.form.get('cliente_nombre').capitalize() #Capitalizamos para que coincida con la key del diccionario.
        if cliente_nombre in clientes:
            return render_template('clientes.html', data=clientes[cliente_nombre])
        else:
            return render_template('clientes.html', error="Cliente no encontrado")
    return render_template('clientes.html') #Para mostrar el formulario inicialmente.

@app.route('/rodrigo', methods=['GET', 'POST'])
def asd():
    return("Este es el endpoint de rodrigo")

if __name__ == '__main__':
    app.run(debug=True)