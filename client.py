import threading
import socket

username = ''

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
    global username
    username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
            global username
            sendTeste(client, username, msg)
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            
def sendTeste(client, username, msg):
    try:
        text = open("texto.txt", "r") 
        d = dict() 
        keyword = msg

        for line in text:
            words = line.strip().split(" ")              
            for word in words: 
                if word in d: 
                    d[word] += 1
                else: 
                    d[word] = 1

        print(d[keyword])
        msg = f'Eu sou o cliente {username} e a palavra "{msg}" apareceu {d[keyword]} vezes no meu arquivo'
        msg = msg.encode('utf-8')
        client.send(msg)
    except:
        return


def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()