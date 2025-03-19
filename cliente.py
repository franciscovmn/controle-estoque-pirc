import socket
import json

def fazer_requisicao(opcao, id_produto=None, nome_produto=None, preco_produto=None):
    try:
        if opcao == 1:  # Cadastrar produto
            dados = {
                'id': id_produto,
                'nome': nome_produto,
                'preco': preco_produto
            }
            # Convertendo os dados para JSON e codificando
            data = json.dumps(dados).encode()
            # Criando a requisição POST com Content-Length
            requisicao = f"POST /produto HTTP/1.1\r\nContent-Length: {len(data)}\r\n\r\n{data.decode()}"

        elif opcao == 2:  # Consultar produto
            if id_produto:
                requisicao = f"GET /produto?id={id_produto} HTTP/1.1\r\n\r\n"
            else:
                raise ValueError("ID do produto é necessário para consulta")

        elif opcao == 3:  # Remover produto
            if id_produto:
                requisicao = f"DELETE /produto?id={id_produto} HTTP/1.1\r\n\r\n"
            else:
                raise ValueError("ID do produto é necessário para remoção")

        else:
            print("Opção inválida")
            return

        # Conexão com o servidor
        host = '127.0.0.1'
        port = 8080
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        cliente_socket.sendall(requisicao.encode())

        resposta = cliente_socket.recv(4096).decode()
        print(f"Resposta do servidor:\n{resposta}")
        cliente_socket.close()

    except Exception as e:
        print(f"Erro: {e}")

# Interação do usuário no cliente
while True:
    print("Escolha uma opção:")
    print("1. Cadastrar produto")
    print("2. Consultar produto")
    print("3. Remover produto")
    print("4. Sair")
    opcao = int(input("Digite o número da opção: "))
    
    if opcao == 1:
        id_produto = int(input("Digite o ID do produto: "))
        nome_produto = input("Digite o nome do produto: ")
        preco_produto = float(input("Digite o preço do produto: "))
        fazer_requisicao(opcao, id_produto, nome_produto, preco_produto)
    
    elif opcao == 2:
        id_produto = int(input("Digite o ID do produto: "))
        fazer_requisicao(opcao, id_produto)
    
    elif opcao == 3:
        id_produto = int(input("Digite o ID do produto: "))
        fazer_requisicao(opcao, id_produto)
    
    elif opcao == 4:
        print("Saindo...")
        break
