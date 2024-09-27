import json
import socket

#Preenche a lista de produtos que representa o estoque do mercado.
def criar_catalogo():
    return [
        {"id": 1, "nome": "Crash titans", "preco": 70, "tentativas": 3},
        {"id": 2, "nome": "GTA San Andreas", "preco": 100, "tentativas": 3},
        {"id": 3, "nome": "Avatar into the inferno", "preco": 60, "tentativas": 3},
        {"id": 4, "nome": "Mortal Combat", "preco": 120, "tentativas": 3}
    ]

#função para comprar e negociação dos produtos
def negociar(produto_id, preco_oferecido, catalogo):

    for produto in catalogo:
        if produto['id'] == produto_id:
            if produto['tentativas'] > 0:
                aux = desconto(produto['preco'],3)

                if preco_oferecido == produto['preco']:
                    return "OKAY! PARABENS PELA COMPRA!!!"
                
                if preco_oferecido >= aux:
                    return "OFERTA ACEITA, ME PECHINCHOU, MAS PODEMOS FECHAR ASSIM"
                else:
                    produto['tentativas'] -= 1
                    produto['preco'] = desconto(produto['preco'],3)
                    resposta = "ESTA OFERTA ESTA MUITO BAIXA, QUE TAL: " + str(produto['preco'])
                    return resposta
                
            else:
                return "Você ja nao pode mais negociar este produto comigo"
                    
    return "PRODUTO_NAO_ENCONTRADO"

#função de calculo para o desconto
def desconto (preco_Produto,valor_Desconto):
    v = preco_Produto
    p = v * valor_Desconto/100
    valor_Final = v-p

    return valor_Final

#função para criar o servidor e começar a rodar o programa na porta desejada.
def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12000)
    server_socket.bind(server_address)
    server_socket.listen()
    print("Servidor aberto")

    catalogo = criar_catalogo()


    while True:
        connection, client_address = server_socket.accept()
        print('Conexão estabelecida com', client_address)

        catalogo_json = json.dumps(catalogo)
        connection.sendall(catalogo_json.encode())

        while True:
            data = connection.recv(1024).decode()
            if not data:
                break
            comando, produto_id, preco_oferecido = data.split(',')
            produto_id, preco_oferecido = int(produto_id), float(preco_oferecido)
            resultado = negociar(produto_id, preco_oferecido, catalogo)
            connection.sendall(resultado.encode())

        connection.close()
        print('Conexão encerrada com', client_address)

if __name__ == "__main__":
    servidor()