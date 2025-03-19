# protocolo_transporte.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from protocolo_aplicacao import ArvoreBinaria, Produto

class ServidorHTTP(BaseHTTPRequestHandler):
    arvore_estoque = ArvoreBinaria()

    def do_GET(self):
        try:
            if self.path.startswith("/produto"):
                params = self.path.split('?')
                if len(params) > 1:
                    query = params[1]
                    if query.startswith('id='):
                        try:
                            id_produto = int(query.split('=')[1])
                            produto = self.arvore_estoque.buscar(id_produto)

                            if produto:
                                self.enviar_resposta(200, json.dumps({
                                    'id': produto.produto.id,
                                    'nome': produto.produto.nome,
                                    'preco': produto.produto.preco
                                }))
                            else:
                                self.enviar_resposta(404, 'Produto não encontrado')
                        except ValueError:
                            self.enviar_resposta(400, 'ID inválido')
                    else:
                        self.enviar_resposta(400, 'Parâmetro "id" faltando')
                else:
                    self.enviar_resposta(400, 'Requisição mal formada')
            else:
                self.enviar_resposta(404, 'Rota não encontrada')
        except Exception as e:
            print(f"Erro ao processar GET: {e}")
            self.enviar_resposta(500, f"Erro interno do servidor: {e}")

    def do_POST(self):
        try:
            if self.path == "/produto":
                conteudo_length = int(self.headers['Content-Length'])
                body = self.rfile.read(conteudo_length)
                dados = json.loads(body)

                id_produto = dados['id']
                nome_produto = dados['nome']
                preco_produto = dados['preco']

                produto = Produto(id_produto, nome_produto, preco_produto)
                self.arvore_estoque.inserir(produto)

                self.enviar_resposta(200, 'Produto cadastrado com sucesso')
            else:
                self.enviar_resposta(404, 'Rota não encontrada')
        except Exception as e:
            print(f"Erro ao processar POST: {e}")
            self.enviar_resposta(500, f"Erro interno do servidor: {e}")

    def do_DELETE(self):
        try:
            if self.path.startswith("/produto"):
                params = self.path.split('?')
                if len(params) > 1:
                    query = params[1]
                    id_produto = int(query.split('=')[1])

                    produto = self.arvore_estoque.buscar(id_produto)
                    if produto:
                        self.arvore_estoque.remover(id_produto)
                        self.enviar_resposta(200, 'Produto removido com sucesso')
                    else:
                        self.enviar_resposta(404, 'Produto não encontrado')
                else:
                    self.enviar_resposta(400, 'Requisição mal formada')
            else:
                self.enviar_resposta(404, 'Rota não encontrada')
        except Exception as e:
            self.enviar_resposta(500, str(e))

    def enviar_resposta(self, status_code, mensagem):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(mensagem.encode())
