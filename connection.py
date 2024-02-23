import os
import socket

send = True
receive = True

host = '192.168.56.1'
port = 5000

def sender_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while send:
        try:
            s.connect((host, port))
            s.sendall(b'Hello, world')
            
            print('Conected to server')
            
            s.close()
            break
        except:
            print('Connection not found. Try again')

def receive_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while receive:
        try:
            s.bind((host, port))
            s.listen()
            client, address = s.accept()
            
            print('Connected to', address)
            
            client.close()
            break
        except:
            print('Connection not found. Try again')


option = 0
while option != 3:
    print('1. Send file to server')
    print('2. Receive file from server')
    print('3. Exit')
    
    option = int(input('Enter an option: '))

    if option == 1:
        sender_connection()
    elif option == 2:
        receive_connection()
    elif option == 3:
        print('Exiting...')
    else:
        print('Invalid option')