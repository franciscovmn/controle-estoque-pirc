import os

# Funções auxiliares
def inicializar_arquivos():
    """Cria arquivos vazios, caso não existam."""
    for arquivo in ["produtos.txt", "clientes.txt", "vendedores.txt", "relatorio.txt"]:
        if not os.path.exists(arquivo):
            with open(arquivo, "w") as f:
                pass

def ler_arquivo(nome_arquivo):
    """Lê dados de um arquivo e retorna uma lista de linhas."""
    with open(nome_arquivo, "r") as f:
        return [linha.strip() for linha in f]

def escrever_arquivo(nome_arquivo, linhas):
    """Sobrescreve um arquivo com as linhas fornecidas."""
    with open(nome_arquivo, "w") as f:
        f.write("\n".join(linhas) + "\n")

def adicionar_linha(nome_arquivo, linha):
    """Adiciona uma linha ao final do arquivo."""
    with open(nome_arquivo, "a") as f:
        f.write(linha + "\n")

# Funções do sistema
def cadastrar_vendedor():
    while True:
        codigo = input("Informe o código do vendedor: ")
        nome = input("Informe o nome do vendedor: ").upper()
        adicionar_linha("vendedores.txt", f"{codigo},{nome},0.00")
        print("Vendedor cadastrado com sucesso!")
        continuar = input("Deseja cadastrar outro vendedor? (s/n): ").lower()
        if continuar != "s":
            break

def cadastrar_produto():
    while True:
        codigo = input("Informe o código do produto: ")
        nome = input("Informe o nome do produto: ").upper()
        preco = float(input("Informe o preço do produto: "))
        quantidade = int(input("Informe a quantidade em estoque: "))
        adicionar_linha("produtos.txt", f"{codigo},{nome},{preco:.2f},{quantidade}")
        print("Produto cadastrado com sucesso!")
        continuar = input("Deseja cadastrar outro produto? (s/n): ").lower()
        if continuar != "s":
            break

def gerenciar_estoque():
    produtos = ler_arquivo("produtos.txt")
    codigo = input("Informe o código do produto para atualizar o estoque: ")
    produto_encontrado = False
    for i, linha in enumerate(produtos):
        dados = linha.split(",")
        if dados[0] == codigo:
            nova_quantidade = int(input(f"Estoque atual: {dados[3]}. Informe a nova quantidade: "))
            dados[3] = str(nova_quantidade)
            produtos[i] = ",".join(dados)
            produto_encontrado = True
            break
    if produto_encontrado:
        escrever_arquivo("produtos.txt", produtos)
        print("Estoque atualizado com sucesso!")
    else:
        print("Produto não encontrado.")

def cadastrar_cliente():
    codigo = input("Informe o código do cliente: ")
    nome = input("Informe o nome do cliente: ").upper()
    adicionar_linha("clientes.txt", f"{codigo},{nome}")
    print("Cliente cadastrado com sucesso!")

def fazer_venda():
    vendedores = ler_arquivo("vendedores.txt")
    codigo_vendedor = input("Informe o código ou nome do vendedor: ").upper()
    vendedor_encontrado = False
    for linha in vendedores:
        if codigo_vendedor in linha:
            vendedor_encontrado = True
            break
    if not vendedor_encontrado:
        print("Vendedor não encontrado. Cadastre o vendedor.")
        cadastrar_vendedor()

    cliente_cadastrado = input("O cliente já possui cadastro? (s/n): ").lower()
    if cliente_cadastrado == "s":
        clientes = ler_arquivo("clientes.txt")
        codigo_cliente = input("Informe o código ou nome do cliente: ").upper()
        cliente_encontrado = any(codigo_cliente in linha for linha in clientes)
        if not cliente_encontrado:
            print("Cliente não encontrado. Cadastre o cliente.")
            cadastrar_cliente()
    else:
        cadastrar_cliente()

    produtos = ler_arquivo("produtos.txt")
    produtos_venda = []
    while True:
        codigo_produto = input("Informe o código ou nome do produto para adicionar à venda: ").upper()
        produto_encontrado = False
        for linha in produtos:
            dados = linha.split(",")
            if codigo_produto in linha:
                produto_encontrado = True
                if int(dados[3]) > 0:
                    quantidade = int(input(f"Informe a quantidade desejada (Estoque: {dados[3]}): "))
                    if quantidade <= int(dados[3]):
                        produtos_venda.append((dados[0], dados[1], float(dados[2]), quantidade))
                        dados[3] = str(int(dados[3]) - quantidade)
                        produtos[produtos.index(linha)] = ",".join(dados)
                        break
                    else:
                        print("Quantidade indisponível em estoque.")
                else:
                    print("Produto sem estoque.")
        if not produto_encontrado:
            print("Produto não encontrado.")
            continuar = input("Deseja tentar novamente? (s/n): ").lower()
            if continuar != "s":
                return

        continuar = input("Deseja adicionar outro produto? (s/n): ").lower()
        if continuar != "s":
            break

    if not produtos_venda:
        print("Nenhum produto adicionado. Venda cancelada.")
        return

    escrever_arquivo("produtos.txt", produtos)

    total_venda = sum(produto[2] * produto[3] for produto in produtos_venda)
    comissao = total_venda * 0.05
    imposto = total_venda * 0.25
    lucro_liquido = total_venda - comissao - imposto

    vendedor_nome = codigo_vendedor if not "," in codigo_vendedor else codigo_vendedor.split(",")[1]
    adicionar_linha("relatorio.txt", f"{total_venda:.2f},{comissao:.2f},{imposto:.2f},{lucro_liquido:.2f},{vendedor_nome}")
    print(f"Venda realizada com sucesso! Total: R${total_venda:.2f}")

def exibir_relatorios():
    relatorio = ler_arquivo("relatorio.txt")
    if not relatorio:
        print("Nenhuma venda registrada.")
        return

    total_vendas = total_comissoes = total_impostos = total_lucro = 0
    print("\nRelatório de Vendas:")
    for linha in relatorio:
        dados = linha.split(",")
        total_vendas += float(dados[0])
        total_comissoes += float(dados[1])
        total_impostos += float(dados[2])
        total_lucro += float(dados[3])
        print(f"Total Venda: R${dados[0]}, Comissão: R${dados[1]}, Imposto: R${dados[2]}, Lucro Líquido: R${dados[3]}, Vendedor: {dados[4]}")

    print("\nResumo:")
    print(f"Total de Vendas: R${total_vendas:.2f}")
    print(f"Total de Comissões: R${total_comissoes:.2f}")
    print(f"Total de Impostos: R${total_impostos:.2f}")
    print(f"Lucro Líquido Total: R${total_lucro:.2f}")

def exibir_menu():
    while True:
        print("\nMenu Inicial")
        print("1. Fazer uma Venda")
        print("2. Outras Atividades Administrativas")
        print("3. Relatórios")
        print("4. Sair do Programa")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            fazer_venda()
        elif opcao == "2":
            print("\n1. Cadastrar Vendedor")
            print("2. Cadastrar Produto")
            print("3. Gerenciar Estoques")
            print("4. Limpar Dados")
            sub_opcao = input("Escolha uma opção: ")
            if sub_opcao == "1":
                cadastrar_vendedor()
            elif sub_opcao == "2":
                cadastrar_produto()
            elif sub_opcao == "3":
                gerenciar_estoque()
            elif sub_opcao == "4":
                limpar_dados()
        elif opcao == "3":
            exibir_relatorios()
        elif opcao == "4":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def limpar_dados():
    for arquivo in ["produtos.txt", "clientes.txt", "vendedores.txt", "relatorio.txt"]:
        with open(arquivo, "w") as f:
            pass
    print("Todos os dados foram apagados.")

# Inicialização do sistema
inicializar_arquivos()
exibir_menu()
