from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from tkinter import filedialog
from ipaddress import ip_address
import socket

def createSearchServer(self):
    frameSearchServer = self.frameSearchServer = CTkFrame(self.root)
    self.toNext(self.frameMenu, frameSearchServer)
    
    labelInstruction = CTkLabel(frameSearchServer, text="Receiver mode", font=("Arial", 18))
    labelInstruction.pack(pady=(10, 0), fill='x', padx=10)
    
    directory_path = ""
    def validData():
        try:
            ip_address(entryHost.get().strip())
            buttonReceiveFile.configure(state='normal' if directory_path else 'disabled')
        except ValueError:
            buttonReceiveFile.configure(state='disabled')
            
    def on_key_press(event):
        validData()
        
    entryHost = CTkEntry(frameSearchServer, font=('Arial', 14), placeholder_text="Server IP address")
    entryHost.pack(pady=(5, 0), padx=10, expand=True, fill='x', ipady=5)
    entryHost.bind("<KeyRelease>", on_key_press)
    
    def saveFileRoute():
        nonlocal directory_path
        directory_path = filedialog.askdirectory()
        if directory_path:
            buttonSelectFolder.configure(text=f"Folder selected: {directory_path.split("/")[-1]}")
        else:
            buttonSelectFolder.configure(text="Click here to selesct a folder")
        
        validData()

    buttonSelectFolder = CTkButton(frameSearchServer, font=('Arial', 14), text="Click here to select a folder", command=lambda: saveFileRoute())
    buttonSelectFolder.pack(pady=(0, 0), padx=10, expand=True, fill='x', ipady=5)
    
    buttonCancel = CTkButton(frameSearchServer, font=('Arial', 14), text="✖️ Cancel", command=lambda: self.toBack(frameSearchServer, self.frameMenu))
    buttonCancel.pack(side='left',  padx=10, pady=10, ipady=5)
    
    buttonReceiveFile = CTkButton(frameSearchServer, font=('Arial', 14), text="Reveive file ✔️", state='disabled', command=lambda: createClient(self, entryHost.get(), directory_path))
    buttonReceiveFile.pack(side='right', padx=10, pady=10, ipady=5)
    
   
def createClient(self, host, directory_path):
    frameClient = self.frameClient = CTkFrame(self.root)
    self.toNext(self.frameSearchServer, frameClient)
    
    frameClient.labelTitle = CTkLabel(frameClient, text="Receiving file", font=("Arial", 18))
    frameClient.labelTitle.pack(pady=(10, 0), fill='x', padx=10)
    
    frameClient.labelInstruction = CTkLabel(frameClient, text="Please wait while the file is being received", font=("Arial", 14))
    frameClient.labelInstruction.pack(pady=(40, 0), fill='x', padx=10)
    
    frameClient.buttonCancel = CTkButton(frameClient, font=('Arial', 14), text="✖️ Cancel", command=lambda: self.toBack(frameClient, self.frameSearchServer))
    frameClient.buttonCancel.pack(side='bottom', pady=10, ipady=5)
    
    receiveFile(self, host, directory_path)
    

def receiveFile(self, host, directory_path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, self.port))
        
        host_name = socket.gethostname()
        s.send(host_name.encode())
        
        code_received = str(s.recv(1024).decode())
        if code_received == '0':
            s.close()
        
        file_name = s.recv(1024).decode()
        file_size = s.recv(1024).decode()
        
        self.frameClient.labelInstruction.configure(text=f"Receiving file {file_name} of {file_size} KB")
        
        file = open(f"{directory_path}/{file_name}", 'wb')
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)
        
        file.close()
        s.close()
        
        self.frameClient.labelTitle.configure(text="File received")
        self.frameClient.labelInstruction.configure(text="File received succesfuly")
        self.frameClient.buttonCancel.configure(text="Go to menu", command=lambda: self.toMenu())
    except socket.error:
        self.frameClient.labelTitle.configure(text="Error")
        self.frameClient.labelInstruction.configure(text="An error ocurred while receiving the file. Please try again.")
        self.frameClient.buttonCancel.configure(text="Try again", command=lambda: self.toBack(self.frameClient, self.frameSearchServer))
    
    
        
    