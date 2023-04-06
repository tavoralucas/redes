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