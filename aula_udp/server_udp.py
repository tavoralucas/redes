import socket
import threading

HOST = '127.0.0.1'  # Endereço IP do Servidor

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
origem = (HOST, 0)  # Escolhe uma porta aleatória para o servidor
udp.bind(origem)
porta = udp.getsockname()[1]
print('Servidor UDP iniciado no IP', HOST, 'na porta', porta)

def handle_client(cliente, data_aniversario):
    dia, mes = data_aniversario.split('/')
    porta_cliente = int('1' + dia + mes)

    for i in range(3):
        # Recebendo as mensagens através do Socket
        mensagem = udp.recvfrom(1024)

        # Exibindo a mensagem recebida
        print('\nCliente:', cliente)
        print('Mensagem:', mensagem.decode())

        # Enviando uma resposta para o cliente
        resposta = 'Mensagem recebida: ' + mensagem.decode()
        destino = (cliente[0], porta_cliente)
        udp.sendto(resposta.encode(), destino)

    print('Finalizando conexão do cliente', cliente)

while True:
    # Recebendo as mensagens através do Socket
    mensagem, cliente = udp.recvfrom(1024)

    # Extraindo a data de aniversário do cliente da mensagem recebida
    data_aniversario = mensagem.decode()

    # Criando uma nova thread para lidar com a conexão
    t = threading.Thread(target=handle_client, args=(cliente, data_aniversario))
    t.start()
