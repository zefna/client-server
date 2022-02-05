import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))
server.listen(5)

clients = []
user_names = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user_name = user_names[index]
            broadcast('{} покинул чат!'.format(user_name).encode('utf-8'))
            user_names.remove(user_name)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Соединение с {}".format(str(address)))

        client.send('NICK'.encode('utf-8'))
        user_name = client.recv(1024).decode('utf-8')
        user_names.append(user_name)
        clients.append(client)

        print("Имя пользователя {}".format(user_name))
        broadcast("{} присоединился!".format(user_name).encode('utf-8'))
        client.send('Присоединился к серверу!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
