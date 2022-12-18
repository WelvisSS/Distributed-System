import os
import math
import socket
import threading
from split_txt import split_txt, create_zips

class Client():
    def __init__(self, host='localhost', port=7777):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockname = None
        self.clientName = None
        self.file_name = None
        self.file_size = None
        self.fileName = input('Digite o nome do arquivo para ser processado: \n')
        self.keyword = input('Digite a palavra para ser buscada: \n')
        self.host = host
        self.port = port
        self.portSize = 2048
        self.listServers = [['localhost', 7777]]
        self.servers = []
        self.numConexoes = len(self.listServers)
        self.numOcorrencias = 0

    def main(self):
        for i in range(self.numConexoes):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.listServers[i][0], self.listServers[i][1]))
                print(f'\nCliente Conectado em {self.listServers[i][0]} na porta {self.listServers[i][1]}!')
            except:
                return print('\nNão foi possível se conectar ao servidor!\n')

            self.servers.append(client)

            thread1 = threading.Thread(target=self.messagesTreatment, args=[client])

            thread1.start()


        if len(self.servers) == self.numConexoes:
            while True:

                res = input('Precione ENTER para iniciar o processamento...\n')
                self.numOcorrencias = 0
                self.broadcastZipFile()

    def broadcastZipFile(self):
        split_txt(f'./{self.fileName}', self.numConexoes)
        create_zips('./split_result', './script.py')

        zips_dir = "./zips"
        file_names = os.listdir(zips_dir)

        count = 0
        # Percorre a lista de clientes que estabeleceram uma coneexão
        for clientItem in self.servers:
            # Para cada cliente individualmente envia uma parte específica para ser processado
            file = open(zips_dir+'/'+file_names[count], 'rb')
            file_size = os.path.getsize(zips_dir+'/'+file_names[count]) 

            msg = f"{count} {file_size} {self.keyword}"

            clientItem.send(str(msg).encode())

            data = file.read()
            clientItem.sendall(data)

            file.close()
            count += 1

    # É acionado quando algum dos clientes envia uma mensagem
    def messagesTreatment(self, client):
        while True:
            try:
                file_name = client.recv(2048).decode()
                file_size = int(client.recv(2048).decode())

                total_packages = 1

                if file_size > 2048:
                    total_packages = math.ceil(file_size/2048)

                file_bytes = b""

                for i in range(total_packages):
                    data = client.recv(2048)
                    file_bytes += data

                file = open(file_name, "wb")        
                file.write(file_bytes)
                file.close()

                # Faz a leitura do resultado obtido no arquivo
                with open(file_name, 'r') as arquivo:
                    result = int(arquivo.read().strip())
                    self.numOcorrencias += result
                    print('Resultados encontrados: ', self.numOcorrencias)

                print('Terminado')
                
            except:
                # self.deleteClient(client)
                break


    def deleteClient(self, client):
        self.servers.remove(client)


Client().main()