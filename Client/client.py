import threading
import socket
import math
from zipfile import ZipFile

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
        print('\nConectado')
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = input('Usuário> ')

    thread1 = threading.Thread(target=receiveMessages, args=[client, username])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client, username):
    while True:

        file_name = client.recv(2048).decode()
        file_size = client.recv(2048).decode()
        keyword = client.recv(2048).decode()
        total_packages = math.ceil(int(file_size)/2048)
        file_bytes = b""

        file = open(file_name, "wb")        

        for i in range(total_packages):
            data = client.recv(2048)
            file_bytes += data

        file.write(file_bytes)
        print('Terminado')
        file.close()

        sendTeste(client, username, file_name, keyword)
            
def sendTeste(client, username, file_name, keyword):
    try:
        total = fileExtract(file_name, keyword)
        msg = f'Eu sou o cliente {username} e recebi o arquivo {file_name} com resultado {total}'
        msg = msg.encode('utf-8')
        client.send(msg)
    except:
        return

def fileExtract(file_name, keyword):

    z = ZipFile('recebido0.zip', 'r')
    z.extractall(path='pasta0')
    z.close()

    text = open("pasta0/livro.txt", "r") 
    d = dict() 

    for line in text:
        words = line.strip().split(" ")          
        for word in words: 
            if word in d: 
                d[word] += 1
            else: 
                d[word] = 1

    return d[keyword]

def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()