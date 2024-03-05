import os
import socket

server = True
client = True

port = 12345

def server_connection():
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.bind((host, port))
    s.listen(1)
    
    print('\n\nServer parameters:')
    print('    Host:', host)
    print('    Port:', port)
    print('\nWaiting for connection...')

    conn, address = s.accept()
    print('Connected to', address)
    
    file = open('Ozelot 1.jpg', 'rb')
    
    conn.send(file.name.encode())
    file_size = str( os.path.getsize(file.name)/1024 ) + ' KB'
    conn.send(file_size.encode())
    
    conn.sendall(file.read())
    
    file.close()
    conn.close()

def client_connection():
    host = ''
    while not validateHost(host):
        host = input('Enter the server IP address: ')
        if not validateHost(host):
            print('Invalid IP address\n')
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((host, port))
        code_received = s.recv(1024).decode()
        if code_received == '0':
            s.close()
            
        file_name = s.recv(1024).decode()
        print('\nReceiving file:', file_name)
        
        file_size = s.recv(1024).decode()
        print('File size:', file_size)
        
        file = open(file_name.replace(".", "_received."), 'wb')
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)
            
        file.close()
        s.close()
            
        print('\nFile received successfully')
    except socket.error:
        print('Connection with the server failed. Verify that the server IP you provided is correct and try again.\n')
        
def validateHost(host):
    try:
        socket.inet_aton(host)
        return True
    except socket.error:
        return False

option = 0
while option != 3:
    print('\n\nOptions:')
    print('1. Send file to server')
    print('2. Receive file from server')
    print('3. Exit')
    
    option = int(input('\nEnter an option: '))

    if option == 1:
        server_connection()
    elif option == 2:
        client_connection()
    elif option == 3:
        print('Exiting...')
    else:
        print('Invalid option')