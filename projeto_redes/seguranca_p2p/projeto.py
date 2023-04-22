import socket
import threading
import time
import sys
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



class myRSA:
    def __init__(self):
        self.name = 'RSA'

    def generate_key_pair(self):
        key = RSA.generate(1024)
        public_key = key.publickey().export_key()
        private_key = key.export_key()
        return (public_key, private_key)

    def encrypt_message(self,message, public_key):
        start_time = time.time()
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        end_time = time.time()
        # print("Encrypt time: ", "{:.4f}".format((end_time - start_time)*1000).replace(".", ","))
        # with open('tempo.txt', 'a') as f:
        #     f.write("{:.4f}".format((end_time - start_time)*1000).replace(".", ",") + '\n')
        return encrypted_message

    def decrypt_message(self,encrypted_message, private_key):
        start_time = time.time()
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
        end_time = time.time()
        # with open('tempo.txt', 'a') as f:
        #     f.write("{:.4f}".format((end_time - start_time)*1000).replace(".", ",") + '\n')
        # print("Decrypt time: ", "{:.4f}".format((end_time - start_time)*1000).replace(".", ","))
        return decrypted_message


class AES:
    def __init__(self):
        self.name = 'AES'
        self.key = b'7-rFP8j-qBEWMt5TUffYVY-r4JHU7VOoi9G9fhT0Qok='
        self.cipher_suite = Fernet(self.key)

    # Função para criptografar uma mensagem
    def encrypt_message(self, msg, rest = None):
        start_time = time.time()
        cipher_text = self.cipher_suite.encrypt(msg.encode('utf-8'))
        end_time = time.time()
        # print("Encrypt time: ",  "{:.4f}".format((end_time - start_time)*1000).replace(".", ","))
        # with open('tempo.txt', 'a') as f:
        #     f.write("{:.4f}".format((end_time - start_time)*1000).replace(".", ",") + '\n')
        return cipher_text

    # Função para descriptografar uma mensagem
    def decrypt_message(self, cipher_text, rest = None):
        start_time = time.time()
        plain_text = self.cipher_suite.decrypt(cipher_text)
        end_time = time.time()
        # print("Decrypt time: ", "{:.4f}".format((end_time - start_time)*1000).replace(".", ","))
        # with open('tempo.txt', 'a') as f:
        #     f.write("{:.4f}".format((end_time - start_time)*1000).replace(".", ",") + '\n')
        return plain_text.decode('utf-8')

rsa = myRSA()
aes = AES()

class User:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        # Defina um par chave pública/chave privada para cada user. Isso não será usado para o remetente, apenas para
        # os destinatários. O remetente apenas solicitará sua chave pública.
        self.public_key = None
        self.private_key = None

    def generate_key_pair(self):
        self.public_key, self.private_key = rsa.generate_key_pair()

# Define a lista de usuários com os quais se deseja se comunicar

USERS = [
    User('Alice', 'localhost', 8001),
    User('Bernardo', 'localhost', 8002),
    User('Caio', 'localhost', 8003)
]

users_by_port = {user.port:user for user in USERS}
users_by_name = {user.name:user for user in USERS}

current_user = None

# Cria o socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

algorithm = None 
algorithm_by_name = {"AES":aes, "RSA": rsa}

def request_public_key(user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((user.ip, user.port))
        s.sendall("PUBLIC_KEY_REQUEST".encode())
        user.public_key = s.recv(1024).decode()
    

# Função que envia uma mensagem para um determinado endereço IP e porta
def send_message(msg, user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #print("Start Time: ", time.time())
        s.connect((user.ip, user.port))
        encrypted_message = algorithm_by_name[algorithm].encrypt_message(msg,user.public_key)
        #print("Message Syze: ", sys.getsizeof(encrypted_message))
        send_time = time.time()
        #print(send_time)
        s.sendall(encrypted_message)

# Função que recebe mensagens de outros usuários e exibe no terminal
def receive_message(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            receiving_time = time.time()
            #print(receiving_time)
            try:
                if data.decode() == "PUBLIC_KEY_REQUEST":
                    conn.sendall(current_user.public_key)
                    return
                elif algorithm == "AES":
                    print(f'\nReceived message from {addr[1]}: {algorithm_by_name[algorithm].decrypt_message(data, current_user.private_key)}')

            except:
                print(f'\nReceived message from {addr[1]}: {algorithm_by_name[algorithm].decrypt_message(data, current_user.private_key)}')

            #print("End Time: ", time.time())

def keep_listening():
    while True:
        # Espera até que algum dos sockets tenha dados de entrada
        conn, addr = sock.accept()
        threading.Thread(target=receive_message, args=(conn, addr)).start()


# Função principal que inicia uma thread para receber mensagens e permite que o usuário envie mensagens
def main():
    print(f'Server running at {HOST}:{PORT}\n')

    while True:   

        # Pede ao usuário para inserir o número de pacotes e o tempo de espera entre pacotes
        num_packets = int(input('Enter number of packets to send: '))
        
        # Verifica se o número de pacotes a enviar é maior que 0
        if num_packets > 0:

            packageParams = []
            recipient_name = input('Enter recipient name: ')
            user = users_by_name[recipient_name]

            if user.public_key is None and algorithm == "RSA":
                request_public_key(user)

            # Espere a chave pública do destinatário ser recebida
            while user.public_key is None and algorithm == "RSA":
                continue

            for i in range(num_packets):
                message_id = int(input('Enter message id (1-6): '))

                message = ''
                if message_id == 1:
                    message = 'Obra na BR-101'
                elif message_id == 2:
                    message = 'Obra na PE-015'
                elif message_id == 3:
                    message = 'Acidente Avenida Norte'
                elif message_id == 4:
                    message = 'Acidente Avenida Cruz Cabugá'
                elif message_id == 5:
                    message = 'Trânsito Intenso na Avenida Boa viagem'
                elif message_id == 6:
                    message = 'Trânsito Intenso na Governador Agamenon Magalhães'
                else:
                    print('Invalid message id')
                    break

                packageParams.append((message, user))

            for packageParam in packageParams:
                threading.Thread(target=send_message, args=packageParam).start()

            
if __name__ == '__main__':

    HOST = 'localhost'
    PORT = int(input("Enter Port: "))

    
    sock.bind((HOST, PORT))
    sock.listen()
    current_user = users_by_port[PORT]
    print(f"You have signed in as {current_user.name}\n")
    # Eu tenho meu par chave privada, chave pública e tenho que solicitar a chave pública dos demais
    current_user.generate_key_pair()

    algorithm = input("Choose the algorithm (AES or RSA): ");

    if algorithm not in ["AES","RSA"]:
        print("Invalid Algorithm Selected")
        exit(0)

    threading.Thread(target=keep_listening).start()
    threading.Thread(target=main).start()
