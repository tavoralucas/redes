#MVP do projeto

import socket

# Define o endereço IP e a porta do servidor
HOST, PORT = '', 8080

# Cria um socket TCP/IP
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar o endereço do socket, caso necessário
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincula o socket ao endereço IP e à porta especificados
listen_socket.bind((HOST, PORT))

# Coloca o socket em modo de escuta para receber conexões
listen_socket.listen(1)

print(f'Servidor WEB aguardando conexões em http://{HOST}:{PORT}...')

while True:
    # Aguarda uma conexão
    client_connection, client_address = listen_socket.accept()

    # Lê a requisição HTTP/1.1 do cliente
    request = client_connection.recv(1024).decode()

    # Extrai a linha de solicitação da requisição HTTP/1.1
    request_line = request.split('\r\n')[0]

    # Extrai o método, o caminho e a versão do protocolo HTTP/1.1
    method, path, version = request_line.split()

    # Verifica se o método é GET
    if method == 'GET':
        # Abre o arquivo solicitado pelo cliente
        try:
            file = open('.' + path, 'rb')
            content = file.read()
            file.close()
            # Define o tipo MIME da resposta HTTP/1.1
            if path.endswith('.html'):
                content_type = 'text/html'
            elif path.endswith('.css'):
                content_type = 'text/css'
            elif path.endswith('.js'):
                content_type = 'application/javascript'
            elif path.endswith('.png'):
                content_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif path.endswith('.gif'):
                content_type = 'image/gif'
            elif path.endswith('.svg'):
                content_type = 'image/svg+xml'
            else:
                content_type = 'application/octet-stream'
            # Define a resposta HTTP/1.1 com o conteúdo do arquivo solicitado
            response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}'.encode()
        except FileNotFoundError:
            # Define a resposta HTTP/1.1 com o código de status 404 (Not Found)
            response = b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n'.encode()
    else:
        # Define a resposta HTTP/1.1 com o código de status 405 (Method Not Allowed)
        response = b'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET\r\nContent-Length: 0\r\n\r\n'.encode()

    # Envia a resposta HTTP/1.1 para o cliente
    client_connection.sendall(response)

    # Encerra a conexão com o cliente
    client_connection.close()