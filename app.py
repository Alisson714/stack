from flask import Flask, render_template, request, jsonify
from calculator import Calculator

app = Flask(__name__)
calc = Calculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        operation = data.get('operation')
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        
        if operation == 'add':
            result = calc.add(a, b)
        elif operation == 'subtract':
            result = calc.subtract(a, b)
        elif operation == 'multiply':
            result = calc.multiply(a, b)
        elif operation == 'divide':
            result = calc.divide(a, b)
        else:
            return jsonify({'error': 'Operación no válida'}), 400
            
        return jsonify({'result': result})
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)