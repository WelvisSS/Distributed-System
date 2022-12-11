import os
import math
import socket
import threading
from zipfile import ZipFile

class Client():
    def __init__(self, host='localhost', port=7777):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockname = None
        self.clientName = None
        self.file_name = None
        self.file_size = None
        self.keyword = None
        self.host = host
        self.port = port
        self.portSize = 2048
        self.file_index = 0

    def main(self):
        try:
            self.client.connect((self.host, self.port))
            print('\nCliente Conectado!')
        except:
            return print('\nNão foi possívvel se conectar ao servidor!\n')

        self.clientName = input('Usuário> ')

        thread1 = threading.Thread(target=self.receiveMessages, args=[])

        thread1.start()
    
    def receiveMessages(self):
        while True:
            
            self.file_index = int(self.client.recv(self.portSize).decode())
            self.file_name = f'recebido{self.file_index}.zip'
            self.file_size = int(self.client.recv(self.portSize).decode())
            self.keyword = self.client.recv(self.portSize).decode()

            total_packages = 1

            if(total_packages > self.portSize):
                total_packages = math.ceil(self.file_size/self.portSize)

            file_bytes = b""
            file = open(self.file_name, "wb")        

            for i in range(total_packages):
                data = self.client.recv(self.portSize)
                file_bytes += data

            file.write(file_bytes)
            file.close()
            print('Preparando o envio do arquivo\n')
            self.sendMessages()

    def sendMessages(self):
        try:
            total = self.fileExtract()

            arquivo = open(f'txt{self.file_index}.txt', 'w')
            arquivo.write(str(total))
            arquivo.close()

            file = open(f'txt{self.file_index}.txt', 'rb')
            data = file.read()
            file.close()
            print('mensagem enviada')

            file_size = os.path.getsize(f'txt{self.file_index}.txt') 
            self.client.send(f'txt{self.file_index}.txt'.encode())
            self.client.send(str(file_size).encode())
            self.client.sendall(data)

        except:
            return

    def fileExtract(self):

        z = ZipFile(f'recebido{self.file_index}.zip', 'r')
        z.extractall(path=f'pasta{self.file_index}')
        z.close()
        from pasta0 import script
        return script.search(f'pasta{self.file_index}/livro.txt', self.keyword)

Client().main()