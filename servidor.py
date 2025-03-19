# servidor.py
from protocolo_transporte import ServidorHTTP
from http.server import HTTPServer

def iniciar_servidor():
    servidor = HTTPServer(('127.0.0.1', 8080), ServidorHTTP)
    print("Servidor rodando em http://127.0.0.1:8080")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
