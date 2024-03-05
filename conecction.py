from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry
from tkinter import filedialog, messagebox

import os, socket, threading
port = 12345
searchConnections_stop = False

root = CTk()
root.title("File sharer")
root.geometry("500x230")
root.resizable(False, False)

framePrincipal = CTkFrame(root)

framePrincipal.pack(pady=10, padx=10, fill='both', expand=True)  
framePrincipal.pack_propagate(False)

# Label for the title
title = CTkLabel(framePrincipal, text="Choice an option", font=("Arial", 18))
title.pack(pady=(25, 10))


# Button share file
buttonShareFile = CTkButton(framePrincipal, font=('Arial', 14), text="Share file", command=lambda: createPreServerPanel())
buttonShareFile.pack(pady=20, padx=20, fill="x", ipady=5)
    
# Button receive file
buttonReceiveFile = CTkButton(framePrincipal, font=('Arial', 14), text="Receive file", command=lambda: createClientPanel())
buttonReceiveFile.pack(padx=20, fill="x", ipady=5)



# Function to create the server panel
def createPreServerPanel():
    framePrincipal.pack_forget()
    
    framePreServer = CTkFrame(root)
    framePreServer.pack(pady=10, padx=10, fill='both', expand=True)
    
    title = CTkLabel(framePreServer, text="Select the file to share", font=("Arial", 18))
    title.pack(pady=(10, 10))
    
    def shareFileRoute():
        global file_path 
        file_path = filedialog.askopenfilename()
        file_name = file_path.split("/")[-1]
        if file_path:
            buttonLoadFile.configure(text=file_name)
        else:
            buttonLoadFile.configure(text="Click here to selesct a file")
        buttonConfirmFile.configure(state='normal' if file_path else 'disabled')
       
    # Button load file 
    buttonLoadFile = CTkButton(framePreServer, font=('Arial', 14), text="Click here to selesct a file", command=lambda: shareFileRoute())
    buttonLoadFile.pack(padx=10, expand=True, fill="x", ipady=5) 
    
    # Button back file
    buttonBack = CTkButton(framePreServer, font=('Arial', 14), text="< Back", command=lambda: toBack(framePrincipal, framePreServer))
    buttonBack.pack(side='left', padx=10, ipady=5)
    
    # Button share file now
    buttonConfirmFile = CTkButton(framePreServer, font=('Arial', 14), text="Send ✔️", command=lambda: createServerPanel(framePreServer, file_path), state='disabled')
    buttonConfirmFile.pack(side='right', pady=10, padx=10, ipady=5)
    
       
    
def createServerPanel(framePreServer: CTkFrame, file_path: str):
    framePreServer.pack_forget()
    
    frameServer = CTkFrame(root)
    frameServer.pack(pady=10, padx=10, fill='both', expand=True)
    
    labelTitle = CTkLabel(frameServer, text="", font=("Arial", 18))
    labelTitle.pack(pady=(15, 0), fill='x', ipady=5)
    
    labelInfo = CTkLabel(frameServer, text="Waiting connections...", font=("Arial", 14))
    labelInfo.pack(pady=(25, 10), fill='x')
    
    def cancel():
        global searchConnections_stop
        searchConnections_stop = True
        if isinstance(s, socket.socket):
            try:
                s.close()
            except Exception as e:
                print(f"An error occurred: {e}")
        toBack(framePreServer, frameServer)
        
    buttonCancel = CTkButton(frameServer, font=('Arial', 14), text="✖️ Cancel", command=lambda: cancel())
    buttonCancel.pack(side="bottom", pady=15, padx=10, ipady=5)
    
    host = socket.gethostbyname(socket.gethostname())
    labelTitle.configure(text=f"{socket.gethostname()} your IP is: {host}")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def searchConnections(s):
        # Function to start the server
        s.bind((host, port))
        s.listen()
    
        global searchConnections_stop
        while not searchConnections_stop:
            try:
                global conn, address 
                conn, address = s.accept()
                
                global host_name
                host_name = conn.recv(1024).decode()
                
                res = messagebox.askyesno("Connection", f"Accept the connection from {host_name} ({address[0]})?")
                if res == False:
                    conn.send("0".encode())
                    conn.close()
                    messagebox.showinfo("Info", "Connection rejected")
                else:
                    buttonCancel.configure(state='disabled')
                    labelInfo.configure(text=f"Sending file to {host_name} ({address[0]})")
                    
                    conn.send("1".encode())
                    
                    # Send the name file
                    file = open(file_path, 'rb')
                    conn.send(file_path.split("/")[-1].encode())
                    
                    # Send the file size
                    file_size = str( os.path.getsize(file.name)/1024 ) + ' KB'
                    conn.send(file_size.encode())
                    
                    # Send the file
                    conn.sendall(file.read())
                    
                    file.close()
                    conn.close()
                    
                    buttonCancel.configure(state='normal')
                    labelInfo.configure(text="Waiting connections...")
                    
            except Exception as e:
                print(f"An error occurred: {e}")
    
    searchConnections_thread = threading.Thread(target=searchConnections, args=(s,))
    searchConnections_thread.start()
    
    

# Function to create the client panel
def createClientPanel():
    framePrincipal.pack_forget()
    
    frameClient = CTkFrame(root)
    frameClient.pack(pady=10, padx=10, fill='both', expand=True)
    
    labelInstruction = CTkLabel(frameClient, text="Receiver mode", font=("Arial", 18))
    labelInstruction.pack(pady=(10, 0), fill='x', padx=10)
    
    entryHost = CTkEntry(frameClient, font=('Arial', 14), placeholder_text="Server IP address")
    entryHost.pack(pady=(5, 0), padx=10, expand=True, fill='x', ipady=5)
    
    def saveFileRoute():
        global directory_path 
        directory_path = filedialog.askdirectory()
        if directory_path:
            buttonSelectFolder.configure(text=f"Folder selected: {directory_path.split("/")[-1]}")
        else:
            buttonSelectFolder.configure(text="Click here to selesct a folder")
        buttonReceiveFile.configure(state='normal' if directory_path else 'disabled')
    
    buttonSelectFolder = CTkButton(frameClient, font=('Arial', 14), text="Click here to select a folder", command=lambda: saveFileRoute())
    buttonSelectFolder.pack(pady=(0, 0), padx=10, expand=True, fill='x', ipady=5)
    
    buttonCancel = CTkButton(frameClient, font=('Arial', 14), text="✖️ Cancel", command=lambda: toBack(framePrincipal, frameClient))
    buttonCancel.pack(side='left',  padx=10, pady=10, ipady=5)
    
    buttonReceiveFile = CTkButton(frameClient, font=('Arial', 14), text="Reveive file ✔️", command=lambda: receiveFile(entryHost.get(), directory_path), state='disabled') 
    buttonReceiveFile.pack(side='right', padx=10, pady=10, ipady=5)
    
    
def receiveFile(host, directory_path):
    try:
        socket.inet_aton(host.strip())
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        host_name = socket.gethostname()
        s.send(host_name.encode())
        
        code_received = str(s.recv(1024).decode())
        if code_received == '0':
            s.close()
        
        file_name = s.recv(1024).decode()
        
        file_size = s.recv(1024).decode()
        
        file = open(f"{directory_path}/{file_name}", 'wb')
        
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)
        
        file.close()
        s.close()
        messagebox.showinfo("Info data", "File received succesfuly")
        
    except socket.error:
        messagebox.showerror("Error", "Invalid IP address or not exist socket connection in the server IP address provided. Verify that the server IP you provided is correct and try again.")
    
    

# Function to back to the previous frame
def toBack(framePrevious: CTkFrame, frameCurrent: CTkFrame):
        frameCurrent.destroy()
        framePrevious.pack(pady=10, padx=10, fill='both', expand=True)
        

root.mainloop() # Start the main loop