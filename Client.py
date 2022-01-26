import socket
import threading
from jdatetime import datetime
#import Server

username = input("enter your username:")

# Check username(ID)
f1 = open('ID client.txt','r')
f1_values = f1.read()
while True:
    if username in f1_values:
        username = input("this username is already in use !! | enter again:")
    else:
        f1.close()
        f2 = open('ID client.txt','a')
        f2.write(f'{username}\n')
        f2.close()
        break

# while True:
#     if username in Server.usernames:
#         username = input("Again enter your name:")
#     else:
#         break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3000))


# receive to Server and Sending username
def listen():
    while True:
        try:
            # listen Message From Server
            # If 'USER' Send username
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        message = f'\n{username}: {input("")} \t\t {datetime.now().strftime("%H:%M:%S | %Y/%m/%d")}'
        client.send(message.encode('ascii'))


# Starting Threads For Listening(receive) And Writing(send)
listen_thread = threading.Thread(target=listen)
listen_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()