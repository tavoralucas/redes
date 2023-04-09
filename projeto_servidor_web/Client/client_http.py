from MySocket import MySocket
import mimetypes
import os

HOST = '127.0.0.1'      # Endereco IP do Servidor
PORT = 8081             # Porta que o Servidor está

print('\nDigite seu path request:')
print('Para sair use CTRL+X\n')

# Recebendo a mensagem do usuário final pelo teclado
mensagem = input()

# Enviando a mensagem para o Servidor TCP através da conexão
while mensagem != '\x18':
    mySocket = MySocket(HOST, PORT)
    mySocket.dispatch(mensagem)
    response = mySocket.listen()

    response_lines = response.split('\r\n')
    status, content_type, content_length, content = response_lines[:4]
    print(status)
    print(content_type)
    print(content_length)
    print(content)
    is_text = content_type.find('text') != -1
    extension = mimetypes.guess_extension(content_type.split(" ")[1])
    print(extension)
    file = open(f'./response{extension}', 'w')
    file.write(content)
    file.close()

    mensagem = input()
    mySocket.close_connection()

