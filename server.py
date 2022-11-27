import threading
import socket

clients = []
numConexoes = 3 
mensagensRecebidas = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Iniciando o servidor no host e porta especificada
        server.bind(('localhost', 7777))
        # Servidor ouvindo
        server.listen()
        print('Servidor rodando!')
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    # Laço que se repete a cada conexão estabelecida
    while True:
        # Recebendo conexões de clientes
        client, addr = server.accept()
        # Adiciona cada novo cliente na lista de clientes
        clients.append(client)
        # Cria uma thread para cada conexão estabelacida
        thread = threading.Thread(target=messagesTreatment, args=[client])
        # Inicia a thread
        thread.start()

        # Quando o número de conexões definido é alcançado, inicia o processo de envio dos arquivos
        if len(clients) == numConexoes:
            while True:
                res = input('Iniciar processamento? (Sim) (Não)\n')
                if res == 'Sim':
                    global mensagensRecebidas
                    mensagensRecebidas = []
                    # Envio dos arquivos para cada cliente conectado
                    broadcastZipFile()
                    # Em quanto as respostas de todos os clientes não chegarem, continua no laço                    
                    while len(mensagensRecebidas) != numConexoes:
                        continue
                elif res == 'M':
                    print(mensagensRecebidas)
                else:
                    print('Operação cancelada')

def broadcastZipFile():
    words = ['dia', 'hoje', 'a']
    count = 0
    # Percorre a lista de clientes que estabeleceram uma coneexão
    for clientItem in clients:
        # Para cada cliente individualmente envia uma parte específica para ser processado
        try:
            value = f'{words[count]}'
            codificando = value.encode('utf-8')
            clientItem.send(codificando)
        except:
            deleteClient(clientItem)
        count += 1

# É acionado quando algum dos clientes envia uma mensagem
def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            msg = msg.decode('utf-8')
            global mensagensRecebidas
            mensagensRecebidas.append(msg)
            print(msg)
            # broadcast(msg, client)
        except:
            deleteClient(client)
            break


def deleteClient(client):
    clients.remove(client)

main()