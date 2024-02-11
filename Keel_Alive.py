from flask import Flask
from threading import Thread

# Configuración
HOST = "0.0.0.0"
PORT = 8080

app = Flask('')

@app.route('/')
def main():
    return "Your SelfBot Is Ready"

def run():
    try:
        app.run(host=HOST, port=PORT)
    except Exception as e:
        print(f"Error: {e}")

def keep_alive():
    """
    Keeps the Flask app alive in a separate thread.
    """
    server = Thread(target=run)
    server.start()

# Ejemplo de uso
if __name__ == "__main__":
    keep_alive()
    # Resto de tu código aquí
  
