from flask import Flask, render_template

app = Flask(__name__)

data = {
    'name': 'Rodrigo Reyes',
    'age': 40,
    'city': 'Santiago'
}

data2 = {
    'name': 'Fernando Cortés',
    'age': 30,
    'city': 'Santiago'
}

@app.route('/')
def index():
    return ("Bienvenido")

@app.route('/rodrigo')
def rodrigo():
    return render_template('index.html', data=data)

@app.route('/fernando')
def fernando():
    return render_template('index.html', data=data2)

if __name__ == '__main__':
    app.run(debug=True)
