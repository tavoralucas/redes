import socket

HOST = '127.0.0.1'  # Endereço IP do Servidor
PORT = 12000  # Porta do Servidor

# Criando o objeto socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Solicitando que o usuário insira o número do dia e do mês do aniversário
dia = input('Digite o dia do seu aniversário (exemplo: 15): ')
mes = input('Digite o mês do seu aniversário (exemplo: 02): ')

# Definindo a porta com base no número do dia e do mês do aniversário
porta_cliente = int('1' + dia + mes)

# Enviando até três mensagens para o servidor
for i in range(3):
    # Solicitando que o usuário digite a mensagem a ser enviada
    mensagem = input(f'Digite a mensagem {i+1}: ')

    # Enviando a mensagem para o servidor
    udp.sendto(mensagem.encode(), (HOST, PORT))

    # Recebendo a resposta do servidor
    resposta = udp.recvfrom(1024)

    # Imprimindo a resposta recebida do servidor
    print(resposta.decode())

# Fechando a conexão
udp.close()
