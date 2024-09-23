# Importar la Flask
from flask import Flask, render_template, request, jsonify
import pandas as pd
import csv

# Función para leer los datos del CSV "Biodiversidad en Boyacá y Cundinamarca.csv"
def leer_datos_CSV():
    datos = []
    with open('Biodiversidad en Boyacá y Cundinamarca.csv', 'r', 
              newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            datos.append(row)
    return datos

# Función para leer el archivo JSON
def leer_datos_JSON():
    df = pd.read_json('Especies_Amenazadas_Boyacá_Cundinamarca.json')
    return df


# Objeto Flask para controlar la aplicación
app_flask = Flask(__name__)


# Configurar las rutas del sitio web
# Congigurar la ruta raiz del sitio para el home
@app_flask.route('/')
def ir_a_principal():
    # return 'Bienvenido a la Página WEB Principal hecha en Flask con Python'
    return render_template('index.html')


@app_flask.route('/cundinamarca')
def ir_a_cundinamarca():
    data = leer_datos_CSV()

    data = [d for d in data if d['DEPARTAMENTO'] == 'Cundinamarca']
    
    clase = request.args.get('clase')
    tipo = request.args.get('tipo')
        
    if clase:
        data = [d for d in data if d['CLASE'] == clase]
    if tipo:
        data = [d for d in data if d['TIPO'] == tipo]

    return render_template('cundinamarca.html', datos = data)

@app_flask.route('/boyaca')
def ir_a_boyaca():
    data = leer_datos_CSV()

    data = [d for d in data if d['DEPARTAMENTO'] == 'Boyacá']
    
    clase = request.args.get('clase')
    tipo = request.args.get('tipo')
        
    if clase:
        data = [d for d in data if d['CLASE'] == clase]
    if tipo:
        data = [d for d in data if d['TIPO'] == tipo]

    return render_template('boyaca.html', datos = data)


# Congigurar la ruta de especies amenazadas
@app_flask.route('/graficos')
def ir_a_graficos():
    # Leer los datos del archivo JSON
    df = leer_datos_JSON()
    
    # Pasar los datos al template como una lista de diccionarios
    datos = df.to_dict(orient='records')
    return render_template('graficos.html', datos=datos)

# Congigurar la ruta de explorar
@app_flask.route('/senderos')
def ir_a_senderos():
    return render_template('senderos.html')

# Ruta para filtrar y devolver datos en formato JSON
@app_flask.route('/filtrar-datos', methods=['GET'])
def filtrar_datos():
    departamento = request.args.get('departamento')
    reino = request.args.get('reino')
    
    try:
        # Asegúrate de que el límite sea un entero válido
        limite = int(request.args.get('limite', 5))
    except ValueError:
        limite = 5

    # Leer los datos del archivo JSON
    df = leer_datos_JSON()

    # Filtrar por departamento y reino
    if departamento:
        df = df[df['Departamento'] == departamento]
    if reino:
        df = df[df['Reino'] == reino]

    # Asegurarse de que el campo 'CBC' está siendo usado
    # Resumir los datos por especie y registros, incluyendo el enlace 'CBC'
    resumen = df.groupby(['Especie', 'CBC'])['Registros'].sum().reset_index()

    # Ordenar por número de registros y limitar
    resumen = resumen.sort_values(by='Registros', ascending=False).head(limite)

    return jsonify(resumen.to_dict(orient='records'))


if __name__ == '__main__':
    app_flask.run(debug=True, port=5000)