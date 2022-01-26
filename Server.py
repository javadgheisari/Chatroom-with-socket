import socket
import threading
from time import sleep
from tqdm import tqdm
from termcolor import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 3000))
server.listen()

clients = []
usernames = []
messages = []

# Send message to all Clients
def send_to_all(message):
    for client in clients:
        client.send(message)


# management message from client to server
def management(client):
    while True:
        try:
            message = client.recv(1024)
            messages.append(message)
            send_to_all(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            send_to_all(f'{username} left the chatroom'.encode('ascii'))
            usernames.remove(username)
            # del from file
            f0 = open('ID client.txt','r')
            lines = f0.readlines()
            f0.close()

            del lines[lines.index(username)]

            new_f0 = open('ID client.txt','w+')
            for line in lines:
                new_f0.write(line)
            new_f0.close()
            break


def receive():
    while True:
        # First join
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(colored(f'username of the client is {username}', 'green'))
        send_to_all(f'{username} joined the chat'.encode('ascii'))
        client.send('You Connected / Welcome'.encode('ascii'))
        client.send(f'\n********************************'.encode('ascii'))

        # Send previously message to new client
        for i in messages:
            client.send(i)
        if len(messages)>0:
            client.send('\n------------- history -------------'.encode('ascii'))

        # One thread for handling client (another messages)
        thread = threading.Thread(target=management, args=(client, ))
        thread.start()

for i in tqdm(range(0, 100), desc ="Server is loading"):
    sleep(.04)
print(colored('Server Started...','green'))

receive()