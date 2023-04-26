# Este código é propriedade de @tavoralucas.
# Todos os direitos são reservados.
# Qualquer uso não autorizado deste código é estritamente proibido.
# percebi algumas pessoas copiando durante alguns momentos adicionei o ofuscamento para evitar cópiaas

import socket
import os
import mimetypes

# Define o endereço IP e a porta do servidor
HOST, PORT = '127.0.0.1', 8081
HTTP_VERSION = 'HTTP/1.1'


def is_inside_private(path):
    private_path = os.path.abspath('private')
    abs_path = os.path.abspath(path)
    return os.path.commonpath([private_path, abs_path]) == private_path

def list_directory(path):

    # Cria a lista de arquivos e pastas presentes na pasta
    files = os.listdir(path)
    files.sort()

    # Cria o conteúdo HTML da página de listagem
    content = "<html><head><title>Index of {0}</title></head><body><h1>Index of {0}</h1><hr><pre>".format(path)
    for f in files:
        link = os.path.join(path, f)
        if os.path.isdir(link):
            f += "/"
        content += '<a href="{0}">{1}</a>\n'.format(link, f)
    content += "</pre><hr></body></html>"

    # Retorna o conteúdo HTML da página de listagem
    return content

def send_error(client_connection, status, message):
    error_page = '<html><head><title>{}</title></head><body><h1>{}</h1><p>{}</p></body></html>'.format(status, status, message)
    headers = [
        '{} {}'.format(HTTP_VERSION, status),
        'Content-Type: text/html',
        'Content-Length: {}'.format(len(error_page))
    ]
    client_connection.send('{}\r\n\r\n'.format('\r\n'.join(headers) +'\r\n'+ error_page).encode())

def handle_request(client_connection):
    # Lê a requisição HTTP/1.1 do cliente
    request = client_connection.recv(1024).decode()

    # Extrai a linha de solicitação da requisição HTTP/1.1
    request_line = request.split('\r\n')[0]

    # Extrai o método, o caminho e a versão do protocolo HTTP/1.1
    request_data = request_line.split()
    if len(request_data) != 3:
        send_error(client_connection, '400 Bad Request', 'Bad Request')
        return

    method, path, version = request_data

    print("Request Data: ",request_data)

    if version != '1.1':
        send_error(client_connection, '505 Version Not Supported', 'A versão do HTTP utilizada não é suportada neste servidor')

    # Verifica se o método é GET
    if method != 'GET':
        send_error(client_connection, '405 Method Not Allowed', 'Method Not Allowed')
        return

    if not os.path.exists(path):
        send_error(client_connection, '404 Not Found', 'File not found')
        return

    response = None

    if is_inside_private(path):
        send_error(client_connection, '403 Forbidden', 'Forbidden')
        return

    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, "index.html")):
            path = f'{path}/index.html'
        elif os.path.isfile(os.path.join(path, "index.hml")):
            path = f'{path}/index.hml'
        else:
            content = list_directory(path)
            content_type = 'text/html'
            response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n{content}'.encode()
            client_connection.send(response)
            return

    # Abre o arquivo solicitado pelo cliente
    try:
        content_type, encoding = mimetypes.guess_type(path)
        is_text = content_type is not None and content_type.startswith('text/')
        file = open(path, 'r' if is_text else 'rb')
        content = file.read()
        file.close()
        # Define o tipo MIME da resposta HTTP/1.1

        if content_type is None:
            content_type = 'application/octet-stream'
        # Define a resposta HTTP/1.1 com o conteúdo do arquivo solicitado
        response = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n{content}'.encode()
    except FileNotFoundError:
        # Define a resposta HTTP/1.1 com o código de status 404 (Not Found)
        send_error(client_connection, '404 Not Found', 'Not Found')
        return

    # Envia a resposta HTTP/1.1 para o cliente
    client_connection.send(response)


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

    print('Client connected: {}'.format(client_address))
    handle_request(client_connection)

    # Encerra a conexão com o cliente
    client_connection.close()