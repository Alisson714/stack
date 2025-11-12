import http.server
import socketserver
import urllib.parse
import json

class Calculator:
    """Clase Calculator con operaciones básicas"""
    
    def add(self, a, b):
        """Suma dos números"""
        return a + b
    
    def subtract(self, a, b):
        """Resta dos números"""
        return a - b
    
    def multiply(self, a, b):
        """Multiplica dos números"""
        return a * b
    
    def divide(self, a, b):
        """Divide dos números"""
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

# Función legacy para compatibilidad
def add(a, b):
    return a + b

class CalculatorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/add':
            query = urllib.parse.parse_qs(parsed_path.query)
            try:
                a = float(query.get('a', ['0'])[0])
                b = float(query.get('b', ['0'])[0])
                result = add(a, b)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'result': result}).encode())
            except (ValueError, TypeError):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid numbers provided'}).encode())
        elif parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <h1>Calculator API</h1>
            <p>Use GET /add?a=2&b=3 to add two numbers</p>
            <p>Example: <a href="/add?a=2&b=3">/add?a=2&b=3</a></p>
            '''
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", 4000), CalculatorHandler) as httpd:
        print("Serving on port 4000")
        httpd.serve_forever()