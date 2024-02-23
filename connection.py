import os
import socket

server = True
client = True

host = 'localhost'
port = 12345

def server_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while server:
        try:
            s.bind((host, port))
            s.listen(1)
            
            
            conn, address = s.accept()
            print('Connected to', address)
            
            message = 'Hello, world'
            conn.send(message.encode())
            
            conn.close()
            break
        except:
            print('Connection not found. Try again')

def client_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while client:
        try:
            s.connect((host, port))
            
            message = s.recv(1024).decode()
            print('Received', message)
            
            s.close()
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
        server_connection()
    elif option == 2:
        client_connection()
    elif option == 3:
        print('Exiting...')
    else:
        print('Invalid option')