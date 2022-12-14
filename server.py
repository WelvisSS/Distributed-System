import os
import math
import socket
import threading

class Server():
    def __init__(self, host='localhost', port=7777):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.mensagensRecebidas = 0
        self.numConexoes = 4
        self.clients = []
        self.numOcorrencias = 0

    def main(self):
        try:
            # Iniciando o servidor no host e porta especificada
            self.server.bind((self.host, self.port))
            # Servidor ouvindo
            self.server.listen()
            print('Servidor rodando!')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        # Laço que se repete a cada conexão estabelecida
        while True:
            # Recebendo conexões de clientes
            client, addr = self.server.accept()
            # Adiciona cada novo cliente na lista de clientes
            self.clients.append(client)
            # Cria uma thread para cada conexão estabelacida
            thread = threading.Thread(target=self.messagesTreatment, args=[client])
            # Inicia a thread
            thread.start()

            # Quando o número de conexões definido é alcançado, inicia o processo de envio dos arquivos
            if len(self.clients) == self.numConexoes:
                while True:

                    res = input('Iniciar processamento? (Sim) (Não)\n')
                    self.numOcorrencias = 0
                    self.broadcastZipFile()

    def broadcastZipFile(self):
        # Palavras que serão buscadas
        keywords = "diferente"
        # Nomes dos arquivos que serão enviados
        fileNames = ['parte1.zip', 'parte2.zip', 'parte2.zip']
        count = 0
        # Percorre a lista de clientes que estabeleceram uma coneexão
        for clientItem in self.clients:
            # Para cada cliente individualmente envia uma parte específica para ser processado
            file = open(fileNames[0], 'rb')
            file_size = os.path.getsize(fileNames[0]) 
    
            # clientItem.send(f"{count}".encode())
            # clientItem.send(str(file_size).encode())
            # clientItem.send(keywords.encode())

            msg = f"{count} {file_size} {keywords}".encode()
            clientItem.send(msg)

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
                    print(self.numOcorrencias)

                # # Apagando o arquivo
                # if os.path.exists(file_name): 
                #     os.remove(file_name)

                print('Terminado')
                
            except:
                self.deleteClient(client)
                break


    def deleteClient(self, client):
        self.clients.remove(client)

Server().main()