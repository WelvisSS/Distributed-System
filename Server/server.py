import os
import math
import socket
import shutil
import threading
import os, subprocess
from zipfile import ZipFile

absolute_path = os.path.dirname(__file__)

class Server():
    def __init__(self, host='localhost', port=7777):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.mensagensRecebidas = 0
        self.numConexoes = 3
        self.clients = []
        self.numOcorrencias = 0
        self.file_index = None
        self.keyword = None
        self.client = None
        self.file_name = None
        self.file_size = None
        self.portSize = 2048

    def main(self):
        try:
            # Iniciando o servidor no host e porta especificada
            self.server.bind((self.host, self.port))
            # Servidor ouvindo
            self.server.listen()
            print(f'Servidor rodando em {self.host} na porta {self.port}\n')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        # Laço que se repete a cada conexão estabelecida
        while True:
            # Recebendo conexões de clientes
            client, addr = self.server.accept()
            # Adiciona cada novo cliente na lista de clientes
            self.clients.append(client)

            self.client = client
            # Cria uma thread para cada conexão estabelacida
            # thread = threading.Thread(target=self.messagesTreatment, args=[client])
            thread = threading.Thread(target=self.receiveMessages, args=[client])
            # Inicia a thread
            thread.start()

            # Quando o número de conexões definido é alcançado, inicia o processo de envio dos arquivos
            print('Conectado!\n')


    def receiveMessages(self, client):
        while True:

            msg = client.recv(self.portSize).decode().split(' ')
            
            self.file_index = int(msg[0])
            self.file_name = f'recebido{self.file_index}.zip'
            self.file_size = msg[1]
            self.keyword = msg[2]

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
                data = client.recv(self.portSize)
                file_bytes += data

            file.write(file_bytes)
            file.close()
            print('Preparando o envio do arquivo\n')
            self.sendMessages(client)

    def sendMessages(self, client):
        
        total = self.fileExtract()

        file_name = f'txt{self.file_index}.txt'

        arquivo = open(file_name, 'w')
        arquivo.write(str(total))
        arquivo.close()

        file = open(file_name, 'rb')
        data = file.read()
        file.close()

        print('mensagem enviada')

        file_size = os.path.getsize(file_name) 
        client.send(file_name.encode())
        client.send(str(file_size).encode())
        client.sendall(data)

        # Apagando o arquivo txt com o resultado
        if os.path.exists(file_name): 
            os.remove(file_name)

    def fileExtract(self):
        global absolute_path
        file_name = f'recebido{self.file_index}.zip'

        # Fazendo a extração do arquivo
        z = ZipFile(file_name, 'r')
        z.extractall(path=f'{absolute_path}/pasta{self.file_index}')
        z.close()
        
        relative_path = f"pasta{self.file_index}/script.py"
        full_path = os.path.join(absolute_path, relative_path)

        txt_path = f'pasta{self.file_index}/livro.txt'
        result = subprocess.run("py \""+full_path+f"\" \"{txt_path}\" {self.keyword}", capture_output=True)
            
        result = result.stdout.decode()
        # Apagando a pasta
        shutil.rmtree(f'pasta{self.file_index}')
        # Apagando o arquivo que foi recebido
        if os.path.exists(file_name): 
            os.remove(file_name)

        return result

        

p = input('Informe a porta para este servidor:\n')
Server(port=int(p)).main()