import json
import socket

#printar o catalogo 
def imprimir_catalogo(catalogo_json):
    catalogo = json.loads(catalogo_json)
    print("Catálogo de produtos:")
    for produto in catalogo:
        print(f"ID: {produto['id']}, Nome: {produto['nome']}, Preço: {produto['preco']}, tentativas: {produto['tentativas']}")

#cria o cliente e o conecta ao servidor
def cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12000)
    client_socket.connect(server_address)

    catalogo_json = client_socket.recv(1024).decode()
    imprimir_catalogo(catalogo_json)

    print("-------------------------------------")
    print("- 1 - COMPRAR -----------------------")
    print("- 2 - LISTAR  -----------------------")
    print("- 3 - SAIR    -----------------------")
    print("-------------------------------------")
    comando = input("Digite o número da operação a realizar: ")

    # este bloco implementa a funcionalidade da negociação no lado de cliente
    if comando == "1":
        while True:
            produto_id = int(input("Digite o ID do produto desejado: "))
            preco_oferecido = float(input("Digite o preço oferecido: "))
            mensagem = f"OFERTA,{produto_id},{preco_oferecido}"
            client_socket.sendall(mensagem.encode())

            resposta = client_socket.recv(1024).decode()
            print(resposta)

            if resposta == "SAIR":
                break
    
    # lista o catalogo
    elif comando == "2":
        imprimir_catalogo(catalogo_json)
    elif comando == "3":
        print("OBRIGADO E VOLTE SEMPRE!")
        client_socket.close()

if __name__ == "__main__":
    cliente()