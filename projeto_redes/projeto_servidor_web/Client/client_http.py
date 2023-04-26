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
    status, content_type, content_length = response_lines[:3]
    data = response_lines[-1].encode('utf-8')  # Assume que o último item é o corpo da resposta

    print(status)
    print(content_type)
    print(content_length)

    is_text = content_type.find('text') != -1

    if not is_text:  # Resposta é um arquivo binário
        extension = mimetypes.guess_extension(content_type.split(" ")[1])
        file = open(f'./response{extension}', 'wb')  # Abre arquivo binário para escrita
        file.write(data)
        file.close()
    else:  # Resposta é um arquivo de texto
        content = data.decode('utf-8')
        extension = mimetypes.guess_extension(content_type.split(" ")[1])
        file = open(f'./response{extension}', 'w')  # Abre arquivo de texto para escrita
        file.write(content)
        file.close()
        print(content)

    mensagem = input()
    mySocket.close_connection()