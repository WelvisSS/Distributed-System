import os
import math
import socket
import shutil
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

            msg = self.client.recv(self.portSize).decode().split(' ')

            print(msg)
            
            self.file_index = int(msg[0])
            self.file_name = f'recebido{self.file_index}.zip'
            self.file_size = msg[1]
            self.keyword = msg[2]

            print(self.file_index)
            print(self.file_name)
            print(self.file_size)
            print(self.keyword)

            total_packages = 1

            total_size_convert = ''
            for caractere in self.file_size:
                if caractere.isdigit():
                    total_size_convert += caractere

            self.file_size = int(total_size_convert)

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

            file_name = f'txt{self.file_index}.txt'

            arquivo = open(file_name, 'w')
            arquivo.write(str(total))
            arquivo.close()

            file = open(file_name, 'rb')
            data = file.read()
            file.close()
            
            # # Apagando o arquivo
            # if os.path.exists(file_name): 
            #     os.remove(file_name)

            print('mensagem enviada')

            file_size = os.path.getsize(file_name) 
            self.client.send(file_name.encode())
            self.client.send(str(file_size).encode())
            self.client.sendall(data)

        except:
            return

    def fileExtract(self):

        file_name = f'recebido{self.file_index}.zip'

        z = ZipFile(file_name, 'r')
        z.extractall(path=f'pasta{self.file_index}')
        z.close()

        from pasta0 import script

        result = script.search(f'pasta{self.file_index}/livro.txt', self.keyword)
        # Apagando a pasta
        shutil.rmtree(f'pasta{self.file_index}')
        # Apagando o arquivo
        # if os.path.exists(file_name): 
        #     os.remove(file_name)

        return result

Client().main()